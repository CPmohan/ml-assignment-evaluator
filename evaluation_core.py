"""Local Ollama rubric evaluator for the U1A1 Linear Regression assignment."""

from __future__ import annotations

import json
import os
import re
from urllib.error import URLError
from urllib.request import Request, urlopen


MAX_TEXT_CHARS = 120_000
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")


def evaluator_provider() -> str:
    """Return the configured evaluator provider; local Ollama is the default."""
    return os.getenv("EVALUATOR_PROVIDER", "ollama").strip().lower()


def ollama_response(
    prompt: str,
    response_format: dict | None = None,
    *,
    seed: int | None = None,
    temperature: float = 0.0,
) -> str:
    """Run one local structured-evaluation request through Ollama's HTTP API."""
    model = os.getenv("OLLAMA_MODEL", "qwen3:4b-instruct").strip()
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful academic evaluator. Return only valid JSON "
                    "matching the requested schema; do not add Markdown fences."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        # 8K covers these short submissions while fitting far better on a 4 GB GPU.
        "options": {
            "temperature": temperature,
            "num_ctx": 8192,
            "num_predict": int(os.getenv("OLLAMA_NUM_PREDICT", "1600")),
        },
    }
    if seed is not None:
        payload["options"]["seed"] = seed
    if response_format:
        payload["format"] = response_format
    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=600) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "Could not contact local Ollama. Start Ollama and confirm the model is installed "
            f"with `ollama list`. Details: {error}"
        ) from error
    content = data.get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("Ollama returned no model response.")
    return content


def parse_json_response(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("The evaluator did not return valid JSON.")
        result = json.loads(text[start:end + 1])
    if not isinstance(result, dict):
        raise ValueError("The evaluator response must be one JSON object.")
    return result


def batch_response_schema(criteria_ids: list[str]) -> dict:
    """Return the strict JSON schema expected from Ollama for a batch response."""
    item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "criterion_id", "score", "decision", "evidence", "feedback", "limitations",
        ],
        "properties": {
            "criterion_id": {"type": "string", "enum": criteria_ids},
            "score": {"type": "integer", "minimum": 0, "maximum": 10},
            "decision": {"type": "string"},
            "evidence": {
                "type": "array",
                "maxItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["page", "text"],
                    "properties": {
                        "page": {"type": "integer", "minimum": 1},
                        "text": {"type": "string", "maxLength": 180},
                    },
                },
            },
            "feedback": {"type": "string", "maxLength": 240},
            "limitations": {"type": "string", "maxLength": 160},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["criteria"],
        "properties": {
            "criteria": {
                "type": "array",
                "minItems": len(criteria_ids),
                "maxItems": len(criteria_ids),
                "items": item,
            },
        },
    }


def evaluate_ml_assignment(
    extracted: dict,
    rubric: dict,
    *,
    seed: int | None = None,
    temperature: float = 0.0,
) -> list[dict]:
    """Evaluate a single submission locally through Ollama."""
    return evaluate_ml_assignment_batch(
        extracted, rubric, seed=seed, temperature=temperature
    )
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Add GEMINI_API_KEY to .env to run the ML assignment evaluator.")

    from crewai import Agent, Crew, LLM, Task

    llm = LLM(
        model=os.getenv("GEMINI_MODEL", "gemini/gemini-3.8-flash"),
        api_key=api_key,
    )
    page_text = "\n\n".join(
        f"[PAGE {page['page']} | embedded_images={page.get('image_count', 0)}]\n{page['text']}"
        for page in extracted["pages"] if page.get("text")
    )
    truncated = len(page_text) > MAX_TEXT_CHARS
    page_text = page_text[:MAX_TEXT_CHARS]
    results = []

    for criterion in rubric["criteria"]:
        maximum = criterion["max_marks"]
        agent = Agent(
            role=f"{criterion['name']} ML assignment evaluator",
            goal=f"Assess the student's work for {criterion['name']} using the supplied rubric.",
            backstory=(
                "You evaluate machine-learning coursework carefully. Distinguish the "
                "assignment prompt, sample answers, and template placeholders from the "
                "student's own response. Use only student work as evidence."
            ),
            llm=llm,
            verbose=False,
        )
        task = Task(
            description=(
                "Evaluate this student's U1A1 Linear Regression assignment for exactly "
                "one rubric criterion. Apply the scoring rule and check correctness, "
                "not just keyword presence. Do not award marks for text copied from the "
                "assignment prompt, sample solution, or an unfilled placeholder. Use "
                "only the student's answer, code, or output. Never invent evidence, "
                "page numbers, results, or execution. Quote a short exact excerpt and "
                "give its PDF page. Award 0 when the student's response is absent or "
                "incorrect; award partial marks only when the rubric supports them; "
                "award full marks only when all required parts are present and correct. "
                "Use whole-number marks for this rubric. If the criterion depends on a "
                "plot, screenshot, or code image that is not readable in extracted text, "
                "return a cautious score and state that visual verification is required. "
                "This is an AI suggestion for a human reviewer, not an approved grade.\n\n"
                f"CRITERION AND SCORING RULE:\n{json.dumps(criterion, ensure_ascii=False)}\n\n"
                f"SUBMISSION TEXT WITH PAGE NUMBERS:\n{page_text}\n\n"
                f"The rubric maximum is {maximum} marks. Return only JSON in this shape:\n"
                f"{{\"criterion_id\":{json.dumps(criterion['id'])},\"score\":0,"
                f"\"max_score\":{maximum},"
                "\"decision\":\"Satisfied / Partially Satisfied / Not Satisfied / Cannot Verify\","
                "\"evidence\":[{\"page\":1,\"text\":\"exact short student-work excerpt\"}],"
                "\"feedback\":\"criterion-specific explanation and next step\","
                "\"limitations\":\"visual or extraction limits, or none\"}"
            ),
            expected_output="One rubric-aligned JSON evaluation for this criterion.",
            agent=agent,
        )
        raw = str(Crew(agents=[agent], tasks=[task], verbose=False).kickoff())
        try:
            result = parse_json_response(raw)
        except (ValueError, json.JSONDecodeError):
            result = {
                "criterion_id": criterion["id"], "score": None,
                "decision": "Cannot Verify", "evidence": [],
                "feedback": "No reliable structured score was returned.",
                "limitations": raw[:1200],
            }

        score = result.get("score")
        if (isinstance(score, bool) or not isinstance(score, (int, float))
                or score < 0 or score > maximum or not float(score).is_integer()):
            result["score"] = None
            result["decision"] = "Cannot Verify"
            result["limitations"] = str(result.get("limitations", "")) + (
                " The score was omitted because it was missing, non-integral, or outside the rubric range."
            )
        result.update({
            "criterion_id": criterion["id"],
            "criterion_name": criterion["name"],
            "max_score": maximum,
            "score_status": "AI suggestion — reviewer approval required",
        })
        if truncated:
            result["limitations"] = str(result.get("limitations", "")) + (
                " Submission text exceeded the evaluator context cap and was truncated."
            )
        results.append(result)
    return results


def evaluate_ml_assignment_batch(
    extracted: dict,
    rubric: dict,
    *,
    seed: int | None = None,
    temperature: float = 0.0,
) -> list[dict]:
    """Evaluate every criterion in one model request for batch processing.

    The output contract and validation match ``evaluate_ml_assignment`` but
    avoid five separate provider calls for every submission.
    """
    page_text = "\n\n".join(
        f"[PAGE {page['page']}]\n{page['text']}"
        for page in extracted["pages"] if page.get("text")
    )
    truncated = len(page_text) > MAX_TEXT_CHARS
    page_text = page_text[:MAX_TEXT_CHARS]
    compact_rubric = [
        {key: item[key] for key in ("id", "name", "max_marks", "expected_evidence", "scoring_rule") if key in item}
        for item in rubric["criteria"]
    ]
    prompt = (
            "Evaluate this U1A1 Linear Regression submission against every rubric "
            "criterion below. Apply each scoring rule, checking correctness rather than "
            "keywords. Do not award marks for text copied from the prompt, sample "
            "solution, or an unfilled placeholder. Use only student work, code, or "
            "output as evidence. Never invent evidence, page numbers, results, or "
            "execution. Award 0 when the student's response is absent or incorrect. "
            "A page marked embedded_images>0 contains visual student work that text extraction "
            "may omit. Do not award zero solely because a plot, code screenshot, or metric "
            "output is not extractable when the student's nearby answer clearly states the "
            "analysis, selected predictor, code method, split, or computed metrics. Award the "
            "rubric credit supported by that answer, record the page, and state that a reviewer "
            "must visually confirm the image. Apply this human-aligned evidence rule: for scatter "
            "analysis, a selected predictor plus a reason earns the analysis credit when image "
            "pages are present; for the sample count and split, a correct stated result earns "
            "credit when image pages indicate omitted code/output; for MAE, MSE, and MAPE, award "
            "one point per metric the student identifies as computed when image pages indicate "
            "omitted results. Do not treat an explicit unfilled placeholder as "
            "evidence. Scores must be whole numbers. Keep each evidence excerpt under "
            "180 characters, feedback under 240 characters, and limitations under 160 characters. "
            "For every criterion, feedback must explain why the awarded score is justified: "
            "name what the student got correct, identify what is incorrect, missing, or "
            "not verifiable, and connect those points to the rubric and score. If full marks "
            "are awarded, state what required work is correct; if zero or partial marks are "
            "awarded, state the specific reason and one useful correction or next step. "
            "Base this explanation only on the cited student evidence and rubric. "
            "Return exactly one item for every rubric criterion.\n\n"
            f"RUBRIC:\n{json.dumps(compact_rubric, ensure_ascii=False)}\n\n"
            f"SUBMISSION TEXT WITH PAGE NUMBERS:\n{page_text}\n\n"
            "Return only one JSON object in exactly this shape:\n"
            "{\"criteria\":[{\"criterion_id\":\"Q1\",\"score\":0,"
            "\"decision\":\"Satisfied / Partially Satisfied / Not Satisfied / Cannot Verify\","
            "\"evidence\":[{\"page\":1,\"text\":\"exact short student-work excerpt\"}],"
            "\"feedback\":\"why this score: correct work, missing or incorrect work, and rubric-linked next step\","
            "\"limitations\":\"visual or extraction limits, or none\"}]}"
    )
    if evaluator_provider() != "ollama":
        raise RuntimeError("This evaluator only supports Ollama. Set EVALUATOR_PROVIDER=ollama.")
    response_schema = batch_response_schema([item["id"] for item in rubric["criteria"]])
    raw = ollama_response(
        prompt, response_schema, seed=seed, temperature=temperature
    )
    if False:  # Legacy cloud implementation retained below temporarily; it is unreachable.
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("Add GEMINI_API_KEY to .env to use the Gemini evaluator.")
        from crewai import Agent, Crew, LLM, Task
        llm = LLM(
            model=os.getenv("GEMINI_MODEL", "gemini/gemini-3.8-flash"),
            api_key=api_key,
        )
        agent = Agent(
            role="ML assignment rubric evaluator",
            goal="Assess each rubric criterion from the supplied student submission.",
            backstory=(
                "You carefully evaluate machine-learning coursework. You distinguish the "
                "assignment prompt and template text from the student's own response."
            ),
            llm=llm,
            verbose=False,
        )
        task = Task(description=prompt,
                    expected_output="One JSON object containing one evaluation for every rubric criterion.",
                    agent=agent)
        raw = str(Crew(agents=[agent], tasks=[task], verbose=False).kickoff())
    try:
        parsed = parse_json_response(raw)
        returned = parsed.get("criteria")
        if not isinstance(returned, list):
            raise ValueError("The evaluator response did not include a criteria list.")
        by_id = {item.get("criterion_id"): item for item in returned if isinstance(item, dict)}
        raw_error = ""
    except (ValueError, json.JSONDecodeError):
        # A local model can occasionally stop mid-object. Retry once with the same
        # schema instead of converting a nearly complete response into five blanks.
        retry_prompt = (
            "Your previous response was incomplete. Return the complete compact JSON "
            "object required below. Do not explain your work outside the JSON.\n\n" + prompt
        )
        retry_raw = ollama_response(
            retry_prompt, response_schema, seed=seed, temperature=temperature
        )
        try:
            parsed = parse_json_response(retry_raw)
            returned = parsed.get("criteria")
            if not isinstance(returned, list):
                raise ValueError("The evaluator response did not include a criteria list.")
            by_id = {item.get("criterion_id"): item for item in returned if isinstance(item, dict)}
            raw_error = ""
        except (ValueError, json.JSONDecodeError):
            by_id = {}
            raw_error = retry_raw[:1200]

    results = []
    for criterion in rubric["criteria"]:
        maximum = criterion["max_marks"]
        result = dict(by_id.get(criterion["id"], {}))
        score = result.get("score")
        if (isinstance(score, bool) or not isinstance(score, (int, float))
                or score < 0 or score > maximum or not float(score).is_integer()):
            result["score"] = None
            result["decision"] = "Cannot Verify"
            result["limitations"] = (str(result.get("limitations", "")) + " " + (
                raw_error or "The score was missing, non-integral, or outside the rubric range."
            )).strip()
        result.update({
            "criterion_id": criterion["id"],
            "criterion_name": criterion["name"],
            "max_score": maximum,
            "score_status": "AI suggestion — reviewer approval required",
        })
        if truncated:
            result["limitations"] = str(result.get("limitations", "")) + (
                " Submission text exceeded the evaluator context cap and was truncated."
            )
        results.append(result)
    return results
