# Specification Template
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

-  in coding_exec.py, Modify the fill_info_prompt function so it completes the coding_agent_prompt in 3 parts. The header which will be used to fill in the information, the charity overview, the research question and the coding scheme, the examples, and lastly the coding scheme.

## Mid-Level Objective

- Modify the fill_info_prompt function so it completes the coding_agent_prompt in 3 parts.
- Modify coding_agent_prompt so that it is 3 strings instead of a single string.

## Implementation Notes
- Only modify the fill_info_prompt function and the coding_agent_prompt.
- Adding the three new strings (coding_agent_prompt_header, coding_agent_prompt_codes, coding_agent_prompt_footer) should be done in the fill_info_prompt function. 
- Adding the three new strings must result in the coding_agent_prompt being a single string that is exactly similar in terms of formatting and content to the original coding_agent_prompt.

## Context

### Beginning context
- coding_exec.py
- coding_prompt.py

### Ending context  
- coding_exec.py
- coding_prompt.py


## Low-Level Tasks
> Ordered from start to finish

1. Modify coding_agent_prompt in 3 different strings
```aider
The first string coding_agent_prompt_header: starts at the beginning of the coding_agent_prompt and ends after the first </Research Question>. Add a skip line after the first string.
The second string coding_agent_prompt_codes: only includes the coding scheme.
The third string coding_agent_prompt_footer: starts at <Examples> and ends at the end of the coding_agent_prompt.
```


2. Modify the fill_info_prompt function so it completes the coding_agent_prompt_header in 3 parts.
```aider
    prompt_with_charity_research_information = coding_agent_prompt_header.format(
        project_description=state['project_description'],
        charity_overview=f"{state['charity_id']}: {state['charity_overview']}",
        research_question=state['research_question']
    )
```

3. Modify the continue_to_invoke_prompt function so it completes the coding_agent_prompt.
```aider
In the send statement, replace "prompt_per_code": prompt_with_charity_research_information.replace("$$code$$", c), with "prompt_per_code": coding_agent_prompt_header + coding_agent_prompt_codes.format("code", c) + coding_agent_prompt_footer,
```
