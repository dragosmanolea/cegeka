from flask import Blueprint, jsonify
from PyPDF2 import PdfReader

cv_blueprint = Blueprint('cv_blueprint', __name__)

reader = PdfReader("cv.pdf")


@cv_blueprint.route('/')
def index():
    if len(reader.pages) > 0:    
        page = reader.pages[0]
        text = page.extract_text()

        return jsonify({
            "text": text
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400

def extract_text():
    page = reader.pages[0]
    text = page.extract_text()
    return text

@cv_blueprint.route('/experience', methods=["GET"])
def get_experience():
    if len(reader.pages) > 0: 
        result = []
        text = extract_text()
        
        projects_and_education = text.split("EXPERIENCES\n")[1]
        projects = projects_and_education.split("EDUCATION")[0]
        individual_projects = projects.split("\n")

        job_title = True
        job_name = ""
        jobs_count = 0

        for job in individual_projects:
            if job_title:
                job_name = job
                result.append({job_name: []})
                job_title = False
            else:
                result[jobs_count][job_name].append(job)
                if job.find("/map_marker") > 0:
                    job_title = True
                    jobs_count += 1

        return jsonify({
            "experience": result
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400


@cv_blueprint.route('/personal', methods=["GET"])
def get_personal():
    if len(reader.pages) > 0: 
        result = {}
        text = extract_text()
        personal = text.split("ACHIEVEMENTS\n")[0].split("\n")
        
        result["name"] = personal[0]
        result["current_position"] = personal[1]
        
        contact_details = personal[2].split("/")
        
        result["email"] = contact_details[1].replace("_475", "")
        result["phone"] = contact_details[2].replace("phone", "")
        result["address"] = contact_details[3].replace("map_marker", "")

        return jsonify({
            "personal": result
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400


@cv_blueprint.route('/education', methods=["GET"])
def get_education():
    if len(reader.pages) > 0:
        result = []
        text = extract_text()

        education = text.split("EDUCATION\n")[1].split("SKILLS\n")[0].split("\n")[:-1]

        new_school = True
        school_count = 0
        school_name = ""

        for edu_info in education:
            if new_school:
                school_name = edu_info
                result.append({edu_info: []})
                new_school = False
            else:
                result[school_count][school_name].append(edu_info)
                if "GPA" in edu_info:
                    new_school = True
                    school_count += 1  

        return jsonify({
            "education": result
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400


@cv_blueprint.route('/achievements', methods=["GET"])
def get_achievements():
    if len(reader.pages) > 0: 
        text = extract_text()

        achievements = text.split("ACHIEVEMENTS")[1].split("HONORS & AWARDS\n")[0].split("\n")[1:-1]
        
        return jsonify({
            "achievements": achievements
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400

@cv_blueprint.route('/awards', methods=["GET"])
def get_awards():
    if len(reader.pages) > 0: 
        text = extract_text()

        awards = text.split("HONORS & AWARDS\n")[1].split("PROJECTS\n")[0].split("\n")[:-1]
        awards = [award.replace('\u2022', "") for award in awards]

        return jsonify({
            "awards": awards
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400

@cv_blueprint.route('/skills', methods=["GET"])
def get_skills():
    if len(reader.pages) > 0: 
        text = extract_text()

        skills = text.split("SKILLS\n")[1].split("EXPERIENCES\n")[0].split("\n")[:-1]

        skills = [skill.replace("\u25cb", "") for skill in skills]
        result = {
            "***": skills[0],
            "**": skills[1],
            "*": skills[2]
        }

        return jsonify({
            "skills": result
        }), 200
    else:
        return jsonify({
            "error": "No page in this PDF"
        }), 400