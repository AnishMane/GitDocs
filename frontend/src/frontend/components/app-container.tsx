
import React, { useState } from "react";
import axios from "axios";
import { RepoForm } from "./repo-form";
import { BlogDisplay } from "./blog-display";
import { LoadingView } from "./loading-view";
import { ErrorMessage } from "./error-message";
import { GitBranch, FileCode, Globe } from "lucide-react";

export const AppContainer: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [blogContent, setBlogContent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateBlog = async (repoUrl: string) => {
    setLoading(true);
    setBlogContent(null);
    setError(null);

    try {
      const response = await axios.post("http://localhost:5000/generate-blog", {
        repo_url: repoUrl,
      });
      
      if (response.data && response.data.blog) {
        setBlogContent(response.data.blog);
      } else {
        setError("Received an invalid response from the server");
      }
    } catch (err: any) {
      console.error("Error generating blog:", err);
      const errorMessage = err.response?.data?.error || 
        "Failed to connect to the backend server. Is it running at http://localhost:5000?";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-github-dark">
      <header className="border-b border-github-border bg-github-darker py-4 px-6">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileCode className="h-6 w-6 text-github-accent" />
            <h1 className="text-xl font-bold text-white">GitDocs</h1>
          </div>
          <div className="flex items-center gap-2">
            <GitBranch className="h-5 w-5 text-github-muted" />
            <span className="text-github-muted text-sm hidden sm:inline">github.com/autodev/blog-wrapper</span>
          </div>
        </div>
      </header>

      <main className="flex-grow py-6 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-github-card border border-github-border rounded-lg shadow-sm p-5 mb-6 animate-fade-in">
            <div className="flex items-center gap-2 mb-4">
              <Globe className="h-5 w-5 text-github-accent" />
              <h2 className="text-lg font-semibold text-github-text">Generate Blog from Repository</h2>
            </div>
            <RepoForm onSubmit={handleGenerateBlog} isLoading={loading} />
          </div>

          {loading ? (
            <div className="bg-github-card border border-github-border rounded-lg shadow-sm animate-fade-in">
              <LoadingView />
            </div>
          ) : error ? (
            <div className="animate-fade-in">
              <ErrorMessage message={error} />
            </div>
          ) : blogContent ? (
            <div className="bg-github-card border border-github-border rounded-lg shadow-sm p-5 animate-fade-in">
              <BlogDisplay content={blogContent} />
            </div>
          ) : null}
        </div>
      </main>

      <footer className="border-t border-github-border bg-github-darker py-4 px-6">
        <div className="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-center sm:justify-between text-sm text-github-muted">
          <div>© {new Date().getFullYear()} GitDocs</div>
          <div className="flex items-center gap-4 mt-2 sm:mt-0">
            {/* <a href="#" className="hover:text-github-accent transition-colors">Documentation</a> */}
            <a href="https://github.com/AnishMane/GitDocs" className="hover:text-github-accent transition-colors">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
};
