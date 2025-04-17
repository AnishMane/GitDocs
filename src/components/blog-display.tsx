
import React from "react";
import { Button } from "@/components/ui/button";
import { Copy, Download } from "lucide-react";
import { MarkdownRenderer } from "./markdown-renderer";
import { toast } from "@/components/ui/use-toast";

interface BlogDisplayProps {
  content: string;
}

export const BlogDisplay: React.FC<BlogDisplayProps> = ({ content }) => {

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      toast({
        title: "Copied to clipboard",
        description: "Blog content has been copied to clipboard",
      });
    } catch (error) {
      toast({
        title: "Failed to copy",
        description: "Could not copy to clipboard",
        variant: "destructive",
      });
    }
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "autodev-blog.md";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast({
      title: "Downloaded",
      description: "Blog saved as autodev-blog.md",
    });
  };

  return (
    <div className="flex flex-col w-full space-y-4">
      <div className="flex flex-row justify-between items-center">
        <h2 className="text-xl font-semibold text-github-text">Generated Blog</h2>
        <div className="flex space-x-2">
          <Button
            onClick={handleCopy}
            variant="outline"
            size="sm"
            className="flex items-center gap-1 border-github-border hover:bg-github-highlight"
          >
            <Copy className="h-4 w-4" />
            <span className="hidden sm:inline">Copy</span>
          </Button>
          <Button
            onClick={handleDownload}
            variant="outline"
            size="sm"
            className="flex items-center gap-1 border-github-border hover:bg-github-highlight"
          >
            <Download className="h-4 w-4" />
            <span className="hidden sm:inline">Download</span>
          </Button>
        </div>
      </div>
      
      <div className="border border-github-border rounded-lg p-4 bg-github-card overflow-auto scrollbar-github max-h-[60vh]">
        <MarkdownRenderer markdown={content} />
      </div>
    </div>
  );
};
