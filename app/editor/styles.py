"""
CSS Styles for Resume Sections

This module defines the CSS classes and styles used to render different
resume sections with consistent formatting in both the editor and PDF export.
"""

# Define CSS styles for different resume section types
RESUME_CSS_STYLES = """
/* Base styles */
.resume-section {
    margin-bottom: 1rem;
}

/* Contact Information - typically bold, larger font */
.resume-contact h3,
.resume-contact .section-title {
    font-size: 1.2em;
    color: #0056b3;
    font-weight: bold;
    margin-top: 0.8rem;
}

.resume-contact p,
.resume-contact .contact-item {
    line-height: 1.4;
}

/* Summary/Objective - usually italic or different font */
.resume-summary h3,
.resume-summary .section-title {
    font-size: 1.2em;
    color: #8a6d3b;
    margin-top: 0.8rem;
}

.resume-summary p,
.resume-summary .summary-text {
    font-style: italic;
    line-height: 1.5;
}

/* Experience - uses bullet points or indents */
.resume-experience h3,
.resume-experience .section-title {
    font-size: 1.2em;
    color: #d04444;
    margin-top: 0.8rem;
}

.resume-experience ul,
.resume-experience ol,
.resume-experience .experience-list {
    padding-left: 1.5rem;
    line-height: 1.6;
}

.resume-experience li,
.resume-experience .experience-item {
    margin-bottom: 0.3rem;
}

/* Education - similar to experience but different color */
.resume-education h3,
.resume-education .section-title {
    font-size: 1.2em;
    color: #4a75b6;
    margin-top: 0.8rem;
}

.resume-education ul,
.resume-education ol,
.resume-education .education-list {
    padding-left: 1.5rem;
    line-height: 1.6;
}

.resume-education li,
.resume-education .education-item {
    margin-bottom: 0.3rem;
}

/* Skills - bullet points, compact */
.resume-skills h3,
.resume-skills .section-title {
    font-size: 1.2em;
    color: #689724;
    margin-top: 0.8rem;
}

.resume-skills ul,
.resume-skills ol,
.resume-skills .skills-list {
    padding-left: 1.5rem;
    line-height: 1.4;
    columns: 2; /* Creates two-column layout for skills */
    -webkit-columns: 2;
    -moz-columns: 2;
}

.resume-skills li,
.resume-skills .skill-item {
    margin-bottom: 0.2rem;
    display: inline-block;
    width: 100%;
}

/* Headings - used for section titles */
.resume-heading {
    font-size: 1.3em;
    color: #2a2a2a;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.resume-list li,
.resume-list .list-item {
    list-style-type: disc;
    margin-left: 0.8rem;
}

/* General paragraph styling */
.resume-section p,
.resume-section .section-content {
    line-height: 1.5;
    margin-bottom: 0.5rem;
}

"""

# Mapping of CSS classes to PDF styles
CSS_TO_PDF_STYLE_MAP = {
    "resume-contact": {
        "title_font_size": 14,
        "title_color": "#0056b3",
        "content_font_size": 12,
        "content_color": "#333333",
        "bullet_char": "-",
        "spacing_after": 0.2 * 72
    },
    "resume-summary": {
        "title_font_size": 14,
        "title_color": "#8a6d3b",
        "content_font_size": 12,
        "content_color": "#555555",
        "bullet_char": "-",
        "spacing_after": 0.2 * 72
    },
    "resume-experience": {
        "title_font_size": 14,
        "title_color": "#d04444",
        "content_font_size": 12,
        "content_color": "#333333",
        "bullet_char": "•",
        "spacing_after": 0.2 * 72
    },
    "resume-education": {
        "title_font_size": 14,
        "title_color": "#4a75b6",
        "content_font_size": 12,
        "content_color": "#333333",
        "bullet_char": "•",
        "spacing_after": 0.2 * 72
    },
    "resume-skills": {
        "title_font_size": 14,
        "title_color": "#689724",
        "content_font_size": 12,
        "content_color": "#333333",
        "bullet_char": "-",
        "spacing_after": 0.2 * 72
    },
    "resume-section": {
        "title_font_size": 14,
        "title_color": "#2a2a2a",
        "content_font_size": 12,
        "content_color": "#333333",
        "bullet_char": "-",
        "spacing_after": 0.2 * 72
    }
}

# Default PDF style for sections without specific CSS class
DEFAULT_PDF_STYLE = {
    "title_font_size": 14,
    "title_color": "#000000",
    "content_font_size": 12,
    "content_color": "#333333",
    "bullet_char": "-",
    "spacing_after": 0.2 * 72
}
