from langrade import constants


def test_prompt_structure():
    prompts = [
        constants.RELEVANCE_PROMPT,
        constants.READABILITY_PROMPT,
        constants.COHERENCE_PROMPT,
    ]

    for prompt in prompts:
        assert "{document}" in prompt
        assert "Binary score (yes/no):" in prompt
        assert "Reasoning:" in prompt


def test_system_prompt():
    assert "You are a grader" in constants.SYSTEM_PROMPT
    assert "binary score" in constants.SYSTEM_PROMPT.lower()


def test_descriptions():
    assert len(constants.REASONING_DESCRIPTION) > 0
    assert "yes" in constants.BINARY_SCORE_DESCRIPTION.lower()
    assert "no" in constants.BINARY_SCORE_DESCRIPTION.lower()
