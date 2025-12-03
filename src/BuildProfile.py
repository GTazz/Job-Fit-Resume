from .__config import PROFILE_MD

class BuildProfile:

    md_profile: str = ""
    def __init__(self, data: dict, debug=False):
        
        self.md_profile = (
            "# User's Data"
            "\n## Personal Info"
            f"\n- Name: {data["Profile"][0].get('Full Name', 'N/A')}"
            f"\n- Headline: {data["Profile"][0].get('Headline', 'N/A')}"
            f"\n- Summary: {data["Profile"][0].get('Summary', 'N/A')}"
            "\n## Projects"
            f"""\n{
                "\n".join([
                f"### {project.get("Title", "N/A")}"
                f"\n- Description: {project.get("Description", "N/A")}" for project in data.get("Projects", [])])
                
            }"""
            "\n## Experience"
            f"""\n{
                "\n".join([
                f"### {position.get("Company Name", "N/A")}"
                f"\n- Title: {position.get("Title", "N/A")}"
                f"\n- Description: {position.get("Description", "N/A")}"
                f"\n- Duration: {position.get("Duration", "N/A")}" for position in data.get("Positions", [])])
            }"""
            "\n## Education"
            f"""\n{
                "\n".join([
                f"### {project.get("School Name", "N/A")} | {project.get("Degree Name", "N/A")}"
                f"\n- Notes: {project.get("Notes", "N/A")}"
                f"\n- Activities: {project.get("Activities", "N/A")}"  
                f"\n- Duration: {project.get("Duration", "N/A")}" for project in data.get("Education", [])])
            }"""
            "\n## Languages"
            f"""\n{
                "\n".join([
                f"- {language}" for language in data.get("Languages", [])
                ])
            }"""
            "\n## Skills"
            f"""\n{
                "\n".join([
                f"- {skill}" for skill in data.get("Skills", [])
                ])
            }"""
            "\n\n---"
        )
        self._save_markdown()

    def _save_markdown(self):
        with open(PROFILE_MD, "w", encoding="utf-8") as f:
            f.write(self.md_profile)

 
if __name__ == "__main__":
    # Testing
    debug = True

    # load data from data/profile.json
    with open("data/profile.json", "r", encoding="utf-8") as f:
        import json
        data = json.load(f)

    BuildProfile(data=data, debug=debug)
