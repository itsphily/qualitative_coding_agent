.PHONY: help test full aider aider-oneshot aider-reflect

# Display help information as default target
help:
	@echo "Available commands:"
	@echo "===================="
	@echo "make help           - Display this help message"
	@echo "make test           - Run a test with minimal parameters"
	@echo "make full           - Run with expanded parameters and all charities"
	@echo "make aider          - Run aider in architect mode with o3-mini"
	@echo "make aider-oneshot  - Run aider once with a prompt file (PROMPT=path/to/file.txt)"
	@echo "make aider-reflect  - Run aider twice: implement changes then verify them (PROMPT=path/to/file.txt)"
	@echo ""
	@echo "Example usage:"
	@echo "  make aider-oneshot PROMPT=prompts.txt"
	@echo "  make aider-reflect PROMPT=prompts.txt"

# Define common variables
PYTHON = uv run

# Test run with minimal parameters
test:
	$(PYTHON) src/coding/coding_exec.py \
		--research_question "What operational processes enable charities to be cost effective?" \
		--code_list \
			"Calibrating the approach: Changing the charity's intervention depending on the specifics of the location." \
			"Pre-intervention data collection: Collecting information about the charitable cause before implementing the charity's intervention." \
		--charities '[{"charity_id": "GiveDirectly", "charity_overview": "Its social goal is '\''Extreme poverty'\''. Its intervention is '\''Distribution of wealth transfers'\''.", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/nougat_extracted_text/01_GiveDirectly_short"}, {"charity_id": "MalariaConsortium", "charity_overview": "Its social goal is '\''Malaria'\''. Its intervention is '\''Distribution of seasonal malaria chemoprevention'\''.", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/04_Malaria_Consortium short"}]'

# Full run with expanded parameters
full:
	$(PYTHON) src/coding/coding_exec.py \
		--research_question "What operational processes enable charities to be cost effective?" \
		--code_list \
			"Calibrating the approach: Changing the charity's intervention depending on the specifics of the location." \
			"Pre-intervention data collection: Collecting information about the charitable cause before implementing the charity's intervention." \
			"Using pilot projects: Using trial projects when the charity enters a new location." \
			"Enhancing capabilities of local stakeholders: Improving the ability of local partners to conduct the intervention." \
			"Securing local buy-in: Ensuring support for the charity's intervention among local stakeholders." \
			"Training local workforce: Improving the skills of the workforce employed by the charity's local partners." \
			"Intra-intervention monitoring: Monitoring the charity's intervention during its implementation." \
			"Imposing standards on local stakeholders: Imposing requirements on the stakeholders involved in the charity's intervention." \
		--charities '[{"charity_id": "GiveDirectly", "charity_overview": "Its social goal is '\''Extreme poverty'\''. Its intervention is '\''Distribution of wealth transfers'\''.", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/01_GiveDirectly"}, {"charity_id": "MalariaConsortium", "charity_overview": "Its social goal is '\''Malaria'\''. Its intervention is '\''Distribution of seasonal malaria chemoprevention'\''.", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/04_Malaria_Consortium"}, {"charity_id": "Deworm the World", "charity_overview": "Its social goal is '\''Schistosomiasis and soil-transmitted helminthiases'\''. Its intervention is '\''Support of deworming programs during school-based mass drug administrations", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/02_deworm_the_world"}, {"charity_id": "Against Malaria Foundation", "charity_overview": "Its social goal is '\''Malaria'\''. Its intervention is '\''Funding and distribution of long-lasting insecticide-treated nets'\''", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/03_Against_Malaria_Foundation"}, {"charity_id": "Schistosomiasis Control Initiative", "charity_overview": "Its social goal is '\''Schistosomiasis and soil-transmitted helminthiases'\''. Its intervention is '\''Support of deworming programs during school-based mass drug administrations'\''", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/05_SCI_Foundation"}, {"charity_id": "Helen Keller International", "charity_overview": "Its social goal is '\''Vitamin A deficiency'\''. Its intervention is '\''Support of government-run vitamin A supplementation program'\''.", "charity_directory": "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/final_markdown_files/06_Hellen_keller"}]'
