"""
Resume Helper - Main Application

A tool to help job seekers tailor their resumes to specific job postings.
This application provides a GUI for uploading resumes, entering job descriptions,
and generating tailored recommendations.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from PIL import Image, ImageTk

# Add the app directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from app.parser.pdf_parser import ResumeParser
from app.analyzer.job_analyzer import JobAnalyzer
from app.comparison.matcher import ResumeMatcher
from app.recommendation.generator import RecommendationGenerator


class ResumeHelperApp:
    """Main application class for Resume Helper."""
    
    def __init__(self, root):
        """
        Initialize the Resume Helper application.
        
        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("Resume Helper")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize variables
        self.resume_path = tk.StringVar()
        self.job_description = tk.StringVar()
        self.resume_data = None
        self.job_requirements = None
        self.comparison_results = None
        self.recommendations = None
        
        # Create the UI components
        self._create_header()
        self._create_input_section()
        self._create_output_section()
        self._create_status_bar()
        
        # Initialize components
        self.parser = ResumeParser()
        self.analyzer = JobAnalyzer()
        self.matcher = ResumeMatcher()
        self.generator = RecommendationGenerator()
    
    def _create_header(self):
        """Create the header section of the UI."""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="Resume Helper", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Tailor your resume to match job descriptions",
            font=("Arial", 10)
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_input_section(self):
        """Create the input section of the UI."""
        input_frame = ttk.LabelFrame(self.main_frame, text="Input")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Resume upload section
        resume_frame = ttk.Frame(input_frame)
        resume_frame.pack(fill=tk.X, padx=10, pady=10)
        
        resume_label = ttk.Label(resume_frame, text="Resume (PDF):")
        resume_label.pack(side=tk.LEFT)
        
        resume_entry = ttk.Entry(resume_frame, textvariable=self.resume_path, width=50)
        resume_entry.pack(side=tk.LEFT, padx=(10, 10))
        
        browse_button = ttk.Button(
            resume_frame, 
            text="Browse...", 
            command=self._browse_resume
        )
        browse_button.pack(side=tk.LEFT)
        
        # Job description section
        job_frame = ttk.Frame(input_frame)
        job_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        job_label = ttk.Label(job_frame, text="Job Description:")
        job_label.pack(anchor=tk.W)
        
        self.job_text = scrolledtext.ScrolledText(job_frame, height=10)
        self.job_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Analyze button
        analyze_frame = ttk.Frame(input_frame)
        analyze_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        analyze_button = ttk.Button(
            analyze_frame,
            text="Analyze and Generate Recommendations",
            command=self._analyze_resume
        )
        analyze_button.pack(side=tk.RIGHT)
    
    def _create_output_section(self):
        """Create the output section of the UI."""
        self.output_notebook = ttk.Notebook(self.main_frame)
        self.output_notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Results tab
        self.results_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.results_frame, text="Results")
        
        # Create a frame for the match score
        match_frame = ttk.Frame(self.results_frame)
        match_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.match_label = ttk.Label(
            match_frame,
            text="Match Score: N/A",
            font=("Arial", 12, "bold")
        )
        self.match_label.pack(side=tk.LEFT)
        
        # Create a frame for the summary
        summary_frame = ttk.LabelFrame(self.results_frame, text="Summary")
        summary_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=3, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.X, padx=5, pady=5)
        self.summary_text.config(state=tk.DISABLED)
        
        # Create a frame for the recommendations
        recommendations_frame = ttk.LabelFrame(self.results_frame, text="Recommendations")
        recommendations_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.recommendations_text = scrolledtext.ScrolledText(recommendations_frame, wrap=tk.WORD)
        self.recommendations_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.recommendations_text.config(state=tk.DISABLED)
        
        # Details tab
        self.details_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.details_frame, text="Details")
        
        # Create a frame for the matches
        matches_frame = ttk.LabelFrame(self.details_frame, text="Matches")
        matches_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.matches_text = scrolledtext.ScrolledText(matches_frame, height=10, wrap=tk.WORD)
        self.matches_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.matches_text.config(state=tk.DISABLED)
        
        # Create a frame for the gaps
        gaps_frame = ttk.LabelFrame(self.details_frame, text="Gaps")
        gaps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.gaps_text = scrolledtext.ScrolledText(gaps_frame, height=10, wrap=tk.WORD)
        self.gaps_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.gaps_text.config(state=tk.DISABLED)
    
    def _create_status_bar(self):
        """Create the status bar at the bottom of the UI."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _browse_resume(self):
        """Open a file dialog to select a resume PDF file."""
        file_path = filedialog.askopenfilename(
            title="Select Resume PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if file_path:
            self.resume_path.set(file_path)
    
    def _analyze_resume(self):
        """Analyze the resume and job description to generate recommendations."""
        # Check if resume is selected
        resume_path = self.resume_path.get()
        if not resume_path:
            messagebox.showerror("Error", "Please select a resume PDF file.")
            return
        
        # Check if job description is entered
        job_description_text = self.job_text.get("1.0", tk.END).strip()
        if not job_description_text:
            messagebox.showerror("Error", "Please enter a job description.")
            return
        
        # Update status
        self.status_var.set("Analyzing resume...")
        self.root.update_idletasks()
        
        try:
            # Parse resume
            self.resume_data = self.parser.parse_resume(resume_path)
            
            # Update status
            self.status_var.set("Analyzing job description...")
            self.root.update_idletasks()
            
            # Analyze job description
            self.job_requirements = self.analyzer.analyze_job_description(job_description_text)
            
            # Update status
            self.status_var.set("Comparing resume to job requirements...")
            self.root.update_idletasks()
            
            # Compare resume to job
            self.comparison_results = self.matcher.compare_resume_to_job(
                self.resume_data,
                self.job_requirements
            )
            
            # Update status
            self.status_var.set("Generating recommendations...")
            self.root.update_idletasks()
            
            # Generate recommendations
            self.recommendations = self.generator.generate_recommendations(
                self.resume_data["raw_text"],
                job_description_text,
                self.comparison_results
            )
            
            # Update status
            self.status_var.set("Analysis complete")
            
            # Display results
            self._display_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred during analysis")
    
    def _display_results(self):
        """Display the analysis results in the UI."""
        if not self.comparison_results or not self.recommendations:
            return
        
        # Update match score
        match_score = self.comparison_results.get("match_score", 0)
        self.match_label.config(text=f"Match Score: {match_score}%")
        
        # Update summary
        summary = self.recommendations.get("summary", "No summary available.")
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)
        
        # Update recommendations
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete("1.0", tk.END)
        
        for rec in self.recommendations.get("recommendations", []):
            priority = rec.get("priority", 0)
            section = rec.get("section", "")
            rec_type = rec.get("type", "")
            content = rec.get("content", "")
            reason = rec.get("reason", "")
            
            self.recommendations_text.insert(tk.END, f"[Priority: {priority}] {section} ({rec_type})\n")
            self.recommendations_text.insert(tk.END, f"{content}\n")
            self.recommendations_text.insert(tk.END, f"Reason: {reason}\n\n")
        
        # Add keyword suggestions
        if "keyword_suggestions" in self.recommendations and self.recommendations["keyword_suggestions"]:
            self.recommendations_text.insert(tk.END, "Suggested Keywords:\n")
            for keyword in self.recommendations["keyword_suggestions"]:
                self.recommendations_text.insert(tk.END, f"- {keyword}\n")
        
        self.recommendations_text.config(state=tk.DISABLED)
        
        # Update matches
        self.matches_text.config(state=tk.NORMAL)
        self.matches_text.delete("1.0", tk.END)
        
        for match in self.comparison_results.get("matches", []):
            category = match.get("category", "").replace("_", " ").title()
            item = match.get("item", "")
            where_found = match.get("where_found", "")
            
            self.matches_text.insert(tk.END, f"{category}: {item}\n")
            self.matches_text.insert(tk.END, f"Found in: {where_found}\n\n")
        
        self.matches_text.config(state=tk.DISABLED)
        
        # Update gaps
        self.gaps_text.config(state=tk.NORMAL)
        self.gaps_text.delete("1.0", tk.END)
        
        for gap in self.comparison_results.get("gaps", []):
            category = gap.get("category", "").replace("_", " ").title()
            item = gap.get("item", "")
            suggestion = gap.get("suggestion", "")
            
            self.gaps_text.insert(tk.END, f"{category}: {item}\n")
            self.gaps_text.insert(tk.END, f"Suggestion: {suggestion}\n\n")
        
        self.gaps_text.config(state=tk.DISABLED)
        
        # Switch to results tab
        self.output_notebook.select(0)


def main():
    """Main function to run the Resume Helper application."""
    root = tk.Tk()
    app = ResumeHelperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
