
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface RepoFormProps {
  onSubmit: (repoUrl: string) => void;
  isLoading: boolean;
}

export const RepoForm: React.FC<RepoFormProps> = ({ onSubmit, isLoading }) => {
  const [repoUrl, setRepoUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (repoUrl.trim()) {
      onSubmit(repoUrl);
    }
  };

  const isValidUrl = (url: string) => {
    return url.trim() !== "" && 
           (url.includes("github.com/") || url.startsWith("https://") || url.startsWith("http://"));
  };

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-4">
      <div className="flex flex-col space-y-2">
        <label htmlFor="repo-url" className="text-sm font-medium text-github-text">
          GitHub Repository URL
        </label>
        <Input
          id="repo-url"
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="https://github.com/username/repository"
          className="bg-github-highlight border-github-border text-github-text focus:border-github-accent focus:ring-github-accent"
          disabled={isLoading}
        />
      </div>
      <Button
        type="submit"
        className="w-full bg-github-accent hover:bg-github-accent/80 text-white"
        disabled={isLoading || !isValidUrl(repoUrl)}
      >
        {isLoading ? "Generating..." : "Generate Blog"}
      </Button>
    </form>
  );
};
