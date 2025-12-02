# Contributing to TopEndSports Content Briefs

## Getting Started

1. Clone the repository
2. Install Claude Code
3. Open the project folder in Claude Code

## Workflow

### Creating a New Content Brief

1. Create a new branch: `git checkout -b brief/topic-name`
2. Use the appropriate workflow:
   - **content-briefs-v1**: Use agent-based system
   - **content-briefs-skill**: Use Claude Code Skill
3. Save your work in the `active/` folder
4. Generated briefs go in `output/`

### Submitting Your Work

1. Commit your changes: `git add . && git commit -m "Add: topic brief"`
2. Push to GitHub: `git push origin brief/topic-name`
3. Create a Pull Request on GitHub
4. Request review from team lead

## File Organization

- **active/**: Work in progress (JSON phase files)
- **output/**: Completed briefs (markdown and docx)
- **data/**: Reference data (site structure, etc.)
- **templates/**: Content templates and guidelines

## Best Practices

- Use descriptive branch names
- Commit frequently with clear messages
- Keep data files updated
- Follow the phase-based workflow
- Request reviews before merging to main

## Questions?

Contact the project maintainer or create an issue on GitHub.
