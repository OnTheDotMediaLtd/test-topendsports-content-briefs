"""
Auto-generated integration script for skill_validation_20260218_071415

Generated: 2026-02-18T07:17:21.633991
Deployment: deploy_skill_validation_20260218_071415_20260218_071721
"""

import yaml
from pathlib import Path
import sys

def integrate_skill(project_dir: Path):
    """
    Integrate skill into project.

    Args:
        project_dir: Path to target project directory
    """
    print(f"Integrating skill_validation_20260218_071415 into {project_dir}")

    # Create skills directory if needed
    skills_dir = project_dir / 'skills'
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy skill file
    skill_file = Path(__file__).parent / 'skill_validation_20260218_071415.yaml'
    target_file = skills_dir / 'skill_validation_20260218_071415.yaml'

    with open(skill_file, 'r') as f:
        skill_data = yaml.safe_load(f)

    with open(target_file, 'w') as f:
        yaml.dump(skill_data, f, default_flow_style=False)

    print(f"[OK] Skill file copied to {target_file}")

    # Create monitoring hook
    create_monitoring_hook(project_dir, skill_data)

    print(f"[OK] Integration complete!")
    print(f"   Skill: skill_validation_20260218_071415")
    print(f"   Location: {target_file}")
    print(f"\nNext steps:")
    print(f"1. Test the integration")
    print(f"2. Enable monitoring")
    print(f"3. Review first results")

def create_monitoring_hook(project_dir: Path, skill_data: dict):
    """Create monitoring hook for skill."""
    hook_file = project_dir / 'scripts' / 'skill_hooks.py'

    hook_code = f'''
# Auto-generated skill hook
def check_skill_validation_20260218_071415(feedback_data):
    """Check if skill_validation_20260218_071415 should be triggered."""
    # Implement trigger logic here
    pass
'''

    # Append to hooks file or create new
    if hook_file.exists():
        with open(hook_file, 'a') as f:
            f.write(hook_code)
    else:
        hook_file.parent.mkdir(parents=True, exist_ok=True)
        with open(hook_file, 'w') as f:
            f.write(hook_code)

    print(f"[OK] Monitoring hook created: {hook_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python integrate_skill.py <project-directory>")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"Error: Project directory not found: {project_path}")
        sys.exit(1)

    integrate_skill(project_path)
