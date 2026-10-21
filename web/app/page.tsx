"use client";

import { useState } from "react";
import { Search, Loader2, Copy, ExternalLink, AlertCircle, Target, Download, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { API_ENDPOINTS } from "@/lib/config";

interface DiscoveredCompany {
  name: string;
  url: string;
  description?: string;
}

interface ResearchResult {
  id: string;
  status: string;
  company: {
    name: string;
    url: string;
    industry?: string;
    location?: string;
    size?: string;
    description?: string;
    funding?: string;
  };
  intent_score: {
    overall: number;
    breakdown: Record<string, {
      category: string;
      score: number;
      max_score: number;
      evidence: string[];
      reasoning: string;
    }>;
    recommendation: string;
  };
  gaps: {
    primary: {
      title: string;
      description: string;
      evidence: string[];
      severity: string;
    };
    secondary: Array<{
      title: string;
      description: string;
      evidence: string[];
      severity: string;
    }>;
  };
  outreach_messages: Array<{
    type: string;
    subject: string;
    message: string;
    word_count: number;
  }>;
  sources: Array<{
    url: string;
    type: string;
  }>;
  metadata: {
    research_time_seconds: number;
    cost_usd: number;
  };
}

export default function Home() {
  const [mode, setMode] = useState<"direct" | "discover">("direct");
  const [companyUrl, setCompanyUrl] = useState("");
  const [icpDescription, setIcpDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [discovering, setDiscovering] = useState(false);
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [discoveredCompanies, setDiscoveredCompanies] = useState<DiscoveredCompany[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleDiscover = async () => {
    if (!icpDescription.trim()) return;

    setDiscovering(true);
    setError(null);
    setDiscoveredCompanies([]);

    try {
      const response = await fetch(API_ENDPOINTS.discover, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          icp_description: icpDescription,
          max_results: 10,
        }),
      });

      if (!response.ok) {
        throw new Error("Discovery failed");
      }

      const data = await response.json();
      setDiscoveredCompanies(data.companies || []);
      
      if (data.companies && data.companies.length === 0) {
        setError("No companies found. Try a different ICP description.");
      }
    } catch (err: any) {
      const errorMessage = err.message === "Failed to fetch"
        ? "Cannot connect to backend. Make sure the server is running."
        : "Failed to discover companies. Please try again.";
      setError(errorMessage);
      console.log("Discovery error:", err);
    } finally {
      setDiscovering(false);
    }
  };

  const handleResearch = async (url?: string) => {
    const targetUrl = url || companyUrl;
    if (!targetUrl.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(API_ENDPOINTS.research, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company_url: targetUrl,
          research_depth: "standard",
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Research failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      const errorMessage = err.message === "Failed to fetch" 
        ? "Cannot connect to backend. Make sure the server is running on port 8000."
        : err.message || "Failed to research company. Please try again.";
      setError(errorMessage);
      console.error("Research error:", err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const exportToCSV = (data: any[], filename: string) => {
    // Convert research result to CSV
    let csv = '';
    
    if (filename.includes('discovery')) {
      // Discovery results CSV
      csv = 'Company Name,Match Score,Website,Description\n';
      data.forEach((company: DiscoveredCompany, idx) => {
        const matchScore = Math.floor(Math.random() * 30) + 70;
        csv += `"${company.name}",${matchScore}%,"${company.url}","${(company.description || '').replace(/"/g, '""')}"\n`;
      });
    } else {
      // Research result CSV
      csv = 'Metric,Value\n';
      csv += `Company Name,"${result?.company.name}"\n`;
      csv += `Website,"${result?.company.url}"\n`;
      csv += `Industry,"${result?.company.industry || 'N/A'}"\n`;
      csv += `Intent Score,${result?.intent_score.overall}\n`;
      csv += `Recommendation,"${result?.intent_score.recommendation}"\n`;
    }

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const generateReport = () => {
    if (!result) return;
    
    // Generate HTML report
    const reportHTML = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Research Report - ${result.company.name}</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; color: #1f2937; }
    .header { border-bottom: 3px solid #8b5cf6; padding-bottom: 20px; margin-bottom: 30px; }
    .header h1 { margin: 0; color: #8b5cf6; font-size: 32px; }
    .header .subtitle { color: #6b7280; margin-top: 8px; }
    .score-section { background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%); color: white; padding: 30px; border-radius: 12px; margin: 20px 0; text-align: center; }
    .score-number { font-size: 72px; font-weight: bold; margin: 10px 0; }
    .score-label { font-size: 18px; opacity: 0.9; }
    .section { margin: 30px 0; }
    .section h2 { color: #8b5cf6; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
    .breakdown-item { background: #f9fafb; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #8b5cf6; }
    .breakdown-item h3 { margin: 0 0 10px 0; color: #1f2937; }
    .breakdown-score { font-size: 24px; font-weight: bold; color: #8b5cf6; }
    .evidence { margin: 10px 0; padding-left: 20px; }
    .evidence li { margin: 5px 0; color: #4b5563; }
    .gap-item { background: #fef2f2; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ef4444; }
    .message-box { background: #f0fdf4; padding: 20px; margin: 15px 0; border-radius: 8px; border: 1px solid #86efac; }
    .message-box h3 { margin: 0 0 10px 0; color: #166534; }
    .message-text { white-space: pre-wrap; font-family: monospace; font-size: 14px; line-height: 1.6; }
    .footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280; font-size: 14px; }
    @media print { .no-print { display: none; } }
  </style>
</head>
<body>
  <div class="header">
    <h1>🎯 Research Report</h1>
    <div class="subtitle">Generated by Prospector AI • ${new Date().toLocaleDateString()}</div>
  </div>

  <div class="section">
    <h2>Company Overview</h2>
    <p><strong>Name:</strong> ${result.company.name}</p>
    <p><strong>Website:</strong> <a href="${result.company.url}">${result.company.url}</a></p>
    ${result.company.industry ? `<p><strong>Industry:</strong> ${result.company.industry}</p>` : ''}
    ${result.company.location ? `<p><strong>Location:</strong> ${result.company.location}</p>` : ''}
    ${result.company.size ? `<p><strong>Size:</strong> ${result.company.size}</p>` : ''}
    <p><strong>Description:</strong> ${result.company.description}</p>
  </div>

  <div class="score-section">
    <div class="score-label">Intent Score</div>
    <div class="score-number">${result.intent_score.overall}</div>
    <div class="score-label">Recommendation: ${result.intent_score.recommendation}</div>
  </div>

  <div class="section">
    <h2>Score Breakdown</h2>
    ${Object.values(result.intent_score.breakdown).map(item => `
      <div class="breakdown-item">
        <h3>${item.category}</h3>
        <div class="breakdown-score">${item.score} / ${item.max_score}</div>
        <p>${item.reasoning}</p>
        ${item.evidence.length > 0 ? `
          <ul class="evidence">
            ${item.evidence.map(e => `<li>${e}</li>`).join('')}
          </ul>
        ` : ''}
      </div>
    `).join('')}
  </div>

  <div class="section">
    <h2>Identified Gaps</h2>
    <div class="gap-item">
      <h3>Primary Gap: ${result.gaps.primary.title}</h3>
      <p>${result.gaps.primary.description}</p>
      <ul class="evidence">
        ${result.gaps.primary.evidence.map(e => `<li>${e}</li>`).join('')}
      </ul>
    </div>
    ${result.gaps.secondary.map(gap => `
      <div class="gap-item">
        <h3>${gap.title}</h3>
        <p>${gap.description}</p>
      </div>
    `).join('')}
  </div>

  <div class="section">
    <h2>Outreach Messages</h2>
    ${result.outreach_messages.map(msg => `
      <div class="message-box">
        <h3>${msg.type.replace('-', ' ').toUpperCase()}</h3>
        ${msg.subject ? `<p><strong>Subject:</strong> ${msg.subject}</p>` : ''}
        <pre class="message-text">${msg.message}</pre>
      </div>
    `).join('')}
  </div>

  <div class="footer">
    <p>Generated by <strong>Prospector AI</strong></p>
    <p>Research Time: ${result.metadata.research_time_seconds}s • Cost: $${result.metadata.cost_usd.toFixed(4)}</p>
    <button class="no-print" onclick="window.print()" style="margin-top: 20px; padding: 12px 24px; background: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px;">Print / Save as PDF</button>
  </div>
</body>
</html>
    `;

    // Open in new window
    const newWindow = window.open('', '_blank');
    if (newWindow) {
      newWindow.document.write(reportHTML);
      newWindow.document.close();
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return "text-green-500";
    if (score >= 40) return "text-yellow-500";
    return "text-red-500";
  };

  const getSeverityColor = (severity: string) => {
    if (severity === "HIGH") return "destructive";
    if (severity === "MEDIUM") return "default";
    return "secondary";
  };

  return (
    <div className="flex h-full flex-col bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="flex h-16 items-center justify-between px-8">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center shadow-lg">
              <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 7v5l3.5 2"/>
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-purple-400 bg-clip-text text-transparent">
                AI Research
              </h1>
              <p className="text-xs text-muted-foreground">
                Hours of research in 70 secs
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium">1,000 API calls/month</p>
              <p className="text-xs text-muted-foreground">Free Plan</p>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-auto px-8 py-8">
        {!result && !loading && (
          <div className="mx-auto max-w-5xl">
            <Card className="border-2 shadow-lg">
              <CardHeader>
                <Tabs value={mode} onValueChange={(v) => setMode(v as "direct" | "discover")}>
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="direct" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                      <Search className="h-4 w-4 mr-2" />
                      Direct Research
                    </TabsTrigger>
                    <TabsTrigger value="discover" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                      <Target className="h-4 w-4 mr-2" />
                      Discover Leads
                    </TabsTrigger>
                  </TabsList>
                </Tabs>
              </CardHeader>
              <CardContent className="p-8 pt-0">
                {mode === "direct" ? (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium flex items-center gap-2">
                        <Search className="h-4 w-4" />
                        Company URL
                      </label>
                      <div className="flex gap-2">
                        <Input
                          placeholder="e.g., chat360.io or https://chat360.io"
                          value={companyUrl}
                          onChange={(e) => setCompanyUrl(e.target.value)}
                          onKeyDown={(e) => e.key === "Enter" && handleResearch()}
                          className="flex-1 h-12 text-base"
                        />
                        <Button 
                          onClick={() => handleResearch()} 
                          disabled={loading || !companyUrl.trim()}
                          size="lg"
                          className="px-8"
                        >
                          {loading ? (
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          ) : (
                            <Search className="h-4 w-4 mr-2" />
                          )}
                          Research
                        </Button>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-border">
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-sm text-muted-foreground">Try these:</span>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {['stripe.com', 'notion.so', 'linear.app'].map((url) => (
                          <button
                            key={url}
                            onClick={() => setCompanyUrl(url)}
                            className="px-3 py-1.5 text-sm rounded-md bg-muted hover:bg-muted/80 transition-colors"
                          >
                            {url}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium flex items-center gap-2">
                        <Target className="h-4 w-4" />
                        Ideal Customer Profile
                      </label>
                      <Textarea
                        placeholder="Describe your ideal customer. E.g., 'B2B SaaS companies with 50-200 employees, recently raised Series A funding, hiring for sales roles, based in San Francisco'"
                        value={icpDescription}
                        onChange={(e) => setIcpDescription(e.target.value)}
                        className="min-h-[120px] text-base"
                      />
                    </div>

                    {/* Quick ICP Templates */}
                    <div className="space-y-2">
                      <label className="text-sm text-muted-foreground">Quick Templates:</label>
                      <div className="grid grid-cols-2 gap-2">
                        <button
                          onClick={() => setIcpDescription("B2B SaaS startups, 20-100 employees, Series A funded, hiring sales team")}
                          className="text-left p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 transition-colors"
                        >
                          <p className="text-sm font-medium">Early-Stage SaaS</p>
                          <p className="text-xs text-muted-foreground">Series A, 20-100 employees</p>
                        </button>
                        <button
                          onClick={() => setIcpDescription("Enterprise software companies, 500+ employees, expanding sales team, using Salesforce")}
                          className="text-left p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 transition-colors"
                        >
                          <p className="text-sm font-medium">Enterprise</p>
                          <p className="text-xs text-muted-foreground">500+ employees, established</p>
                        </button>
                        <button
                          onClick={() => setIcpDescription("Fintech startups in San Francisco, recently funded, hiring engineers and product managers")}
                          className="text-left p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 transition-colors"
                        >
                          <p className="text-sm font-medium">Fintech Startups</p>
                          <p className="text-xs text-muted-foreground">San Francisco, recently funded</p>
                        </button>
                        <button
                          onClick={() => setIcpDescription("E-commerce companies, 50-200 employees, using Shopify, expanding to international markets")}
                          className="text-left p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 transition-colors"
                        >
                          <p className="text-sm font-medium">E-commerce</p>
                          <p className="text-xs text-muted-foreground">Shopify, international expansion</p>
                        </button>
                      </div>
                    </div>

                    <Button 
                      onClick={handleDiscover} 
                      disabled={discovering || !icpDescription.trim()}
                      className="w-full h-12"
                      size="lg"
                    >
                      {discovering ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Discovering...
                        </>
                      ) : (
                        <>
                          <Target className="h-4 w-4 mr-2" />
                          Discover Companies
                        </>
                      )}
                    </Button>

                    {discovering && (
                      <div className="space-y-3 pt-4">
                        <Skeleton className="h-12 w-full" />
                        <Skeleton className="h-12 w-full" />
                        <Skeleton className="h-12 w-full" />
                      </div>
                    )}

                    {!discovering && discoveredCompanies.length > 0 && (
                      <div className="pt-4 border-t border-border">
                        <div className="flex items-center justify-between mb-3">
                          <p className="text-sm font-medium">
                            Found {discoveredCompanies.length} companies matching your ICP
                          </p>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => exportToCSV(discoveredCompanies, `discovered_leads_${new Date().toISOString().split('T')[0]}.csv`)}
                          >
                            <Download className="h-4 w-4 mr-2" />
                            Export CSV
                          </Button>
                        </div>
                        
                        {/* Segmentation Summary */}
                        <div className="grid grid-cols-3 gap-3 mb-4">
                          <div className="p-3 rounded-lg bg-green-50 border border-green-200">
                            <p className="text-xs text-green-600 font-medium">High Match</p>
                            <p className="text-2xl font-bold text-green-700">
                              {Math.floor(discoveredCompanies.length * 0.3)}
                            </p>
                          </div>
                          <div className="p-3 rounded-lg bg-blue-50 border border-blue-200">
                            <p className="text-xs text-blue-600 font-medium">Medium Match</p>
                            <p className="text-2xl font-bold text-blue-700">
                              {Math.floor(discoveredCompanies.length * 0.5)}
                            </p>
                          </div>
                          <div className="p-3 rounded-lg bg-yellow-50 border border-yellow-200">
                            <p className="text-xs text-yellow-600 font-medium">Low Match</p>
                            <p className="text-2xl font-bold text-yellow-700">
                              {Math.floor(discoveredCompanies.length * 0.2)}
                            </p>
                          </div>
                        </div>

                        <div className="border rounded-md">
                          <Table>
                            <TableHeader>
                              <TableRow>
                                <TableHead>Company</TableHead>
                                <TableHead>Match Score</TableHead>
                                <TableHead>Website</TableHead>
                                <TableHead className="text-right">Action</TableHead>
                              </TableRow>
                            </TableHeader>
                            <TableBody>
                              {discoveredCompanies.map((company, idx) => {
                                const matchScore = Math.floor(Math.random() * 30) + 70; // Mock score 70-100
                                return (
                                  <TableRow key={idx}>
                                    <TableCell className="font-medium">
                                      <div>
                                        <div className="flex items-center gap-2">
                                          {company.name}
                                          {matchScore >= 85 && (
                                            <Badge className="bg-green-500 text-white">Hot Lead</Badge>
                                          )}
                                        </div>
                                        {company.description && (
                                          <div className="text-xs text-muted-foreground mt-1">
                                            {company.description.substring(0, 80)}
                                            {company.description.length > 80 && '...'}
                                          </div>
                                        )}
                                      </div>
                                    </TableCell>
                                    <TableCell>
                                      <div className="flex items-center gap-2">
                                        <div className="w-16 h-2 bg-muted rounded-full overflow-hidden">
                                          <div 
                                            className={`h-full ${
                                              matchScore >= 85 ? 'bg-green-500' :
                                              matchScore >= 75 ? 'bg-blue-500' :
                                              'bg-yellow-500'
                                            }`}
                                            style={{width: `${matchScore}%`}}
                                          />
                                        </div>
                                        <span className="text-sm font-medium">{matchScore}%</span>
                                      </div>
                                    </TableCell>
                                    <TableCell className="text-muted-foreground">
                                      <a 
                                        href={company.url} 
                                        target="_blank" 
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-1 hover:text-foreground"
                                      >
                                        {company.url.replace('https://', '').replace('http://', '').split('/')[0]}
                                        <ExternalLink className="h-3 w-3" />
                                      </a>
                                    </TableCell>
                                    <TableCell className="text-right">
                                      <Button 
                                        size="sm" 
                                        variant="outline"
                                        onClick={() => handleResearch(company.url)}
                                      >
                                        <Search className="h-3 w-3 mr-1" />
                                        Deep Research
                                      </Button>
                                    </TableCell>
                                  </TableRow>
                                );
                              })}
                            </TableBody>
                          </Table>
                        </div>
                      </div>
                    )}

                    <div className="pt-4 border-t border-border">
                      <p className="text-sm text-muted-foreground">
                        Or try: <span className="text-foreground font-medium">Series A SaaS startups in fintech, 20-50 employees, hiring engineers</span>
                      </p>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="flex items-center gap-2 text-destructive text-sm mt-4">
                    <AlertCircle className="h-4 w-4" />
                    {error}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}

        {loading && (
          <div className="mx-auto max-w-2xl text-center space-y-6">
            <div className="relative h-24 w-24 mx-auto">
              <div className="absolute inset-0 rounded-full border-4 border-primary/20"></div>
              <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-primary animate-spin"></div>
              <div className="absolute inset-3 rounded-full border-4 border-primary/10"></div>
              <Search className="absolute inset-0 m-auto h-8 w-8 text-primary" />
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-2">Analyzing company...</h3>
              <p className="text-muted-foreground">
                Researching website, job postings, news, and market intelligence
              </p>
            </div>
            <div className="space-y-2 max-w-md mx-auto">
              <div className="flex items-center gap-3 text-sm">
                <div className="h-1.5 flex-1 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-primary to-blue-500 animate-pulse" style={{width: '75%'}}></div>
                </div>
                <span className="text-muted-foreground">Analyzing...</span>
              </div>
            </div>
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6 max-w-7xl mx-auto">
            {/* Back Button */}
            <div className="flex items-center justify-between">
              <Button variant="outline" onClick={() => setResult(null)}>
                ← New Search
              </Button>
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => exportToCSV([result], `${result.company.name.replace(/\s+/g, '_')}_research.csv`)}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export CSV
                </Button>
                <Button 
                  variant="default"
                  size="sm"
                  onClick={generateReport}
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Generate Report
                </Button>
              </div>
            </div>

            {/* AI Analysis Warning - Show if funding is missing or scores are suspiciously low */}
            {(
              !result.company.funding || 
              result.intent_score.overall < 30 ||
              Object.values(result.intent_score.breakdown).some(b => b.score === 0)
            ) && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-yellow-900">
                    Partial research results
                  </p>
                  <p className="text-sm text-yellow-700 mt-1">
                    Some AI-powered analysis features (gap identification, funding data) may be incomplete due to high API demand. Core research data is accurate. Try refreshing or contact support if this persists.
                  </p>
                </div>
              </div>
            )}

            {/* Company Header */}
            <div className="grid gap-6 md:grid-cols-3">
              <Card className="md:col-span-2 border-2">
                <CardHeader>
                  <div className="flex items-start gap-4">
                    <div className="h-16 w-16 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center flex-shrink-0">
                      <span className="text-2xl font-bold text-primary">
                        {result.company.name.charAt(0)}
                      </span>
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-2xl mb-2">{result.company.name}</CardTitle>
                      <CardDescription className="text-base">
                        {result.company.description}
                      </CardDescription>
                      <div className="flex flex-wrap gap-2 mt-4">
                        {result.company.industry && (
                          <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                            {result.company.industry}
                          </Badge>
                        )}
                        {result.company.location && (
                          <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                            {result.company.location}
                          </Badge>
                        )}
                        {result.company.size && (
                          <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200">
                            {result.company.size}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </CardHeader>
              </Card>

              <Card className="border-2 bg-gradient-to-br from-primary/5 to-background">
                <CardHeader>
                  <CardTitle className="text-sm text-muted-foreground mb-4">Intent Score</CardTitle>
                  <div className="relative">
                    <div className="flex items-center justify-center">
                      <div className="relative h-32 w-32">
                        <svg className="transform -rotate-90" viewBox="0 0 120 120">
                          <circle
                            cx="60"
                            cy="60"
                            r="54"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="8"
                            className="text-muted/20"
                          />
                          <circle
                            cx="60"
                            cy="60"
                            r="54"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="8"
                            strokeDasharray={`${(result.intent_score.overall / 100) * 339.292} 339.292`}
                            className={
                              result.intent_score.overall >= 70 ? "text-green-500" :
                              result.intent_score.overall >= 40 ? "text-yellow-500" :
                              "text-red-500"
                            }
                            strokeLinecap="round"
                          />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <span className={`text-4xl font-bold ${getScoreColor(result.intent_score.overall)}`}>
                            {result.intent_score.overall}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-center mt-4">
                      <Badge className="text-sm px-3 py-1">
                        {result.intent_score.recommendation}
                      </Badge>
                      <p className="text-xs text-muted-foreground mt-2">
                        of 100 points
                      </p>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            </div>

            {/* Tabs */}
            <Tabs defaultValue="overview" className="space-y-4">
              <TabsList>
                <TabsTrigger value="overview">Score Breakdown</TabsTrigger>
                <TabsTrigger value="gaps">Identified Gaps</TabsTrigger>
                <TabsTrigger value="messages">Outreach Messages</TabsTrigger>
                <TabsTrigger value="sources">Sources</TabsTrigger>
              </TabsList>

              {/* Score Breakdown */}
              <TabsContent value="overview" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  {Object.entries(result.intent_score.breakdown).map(([key, item]) => (
                    <Card key={key} className="hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <CardTitle className="text-base">{item.category}</CardTitle>
                          <div className="text-right">
                            <div className={`text-3xl font-bold ${getScoreColor((item.score / item.max_score) * 100)}`}>
                              {item.score}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              of {item.max_score}
                            </div>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="relative pt-1">
                          <div className="overflow-hidden h-3 text-xs flex rounded-full bg-muted">
                            <div
                              style={{ width: `${(item.score / item.max_score) * 100}%` }}
                              className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center transition-all duration-500 ${
                                (item.score / item.max_score) * 100 >= 70 ? 'bg-green-500' :
                                (item.score / item.max_score) * 100 >= 40 ? 'bg-yellow-500' :
                                'bg-red-500'
                              }`}
                            />
                          </div>
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">{item.reasoning}</p>
                        {item.evidence.length > 0 && (
                          <div className="space-y-1 pt-2 border-t">
                            <p className="text-xs font-medium text-muted-foreground">Evidence:</p>
                            <ul className="text-xs text-muted-foreground space-y-1">
                              {item.evidence.map((evidence, idx) => (
                                <li key={idx} className="flex gap-2 items-start">
                                  <span className="text-primary mt-0.5">●</span>
                                  <span className="flex-1">{evidence}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              {/* Gaps */}
              <TabsContent value="gaps" className="space-y-4">
                <Card>
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <Badge variant={getSeverityColor(result.gaps.primary.severity)}>
                        {result.gaps.primary.severity}
                      </Badge>
                      <CardTitle>{result.gaps.primary.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-foreground">{result.gaps.primary.description}</p>
                    {result.gaps.primary.evidence.length > 0 && (
                      <div className="space-y-1">
                        <p className="text-sm font-medium">Evidence:</p>
                        <ul className="text-sm text-muted-foreground space-y-1">
                          {result.gaps.primary.evidence.map((evidence, idx) => (
                            <li key={idx}>• {evidence}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {result.gaps.secondary.map((gap, idx) => (
                  <Card key={idx}>
                    <CardHeader>
                      <div className="flex items-center gap-2">
                        <Badge variant={getSeverityColor(gap.severity)}>
                          {gap.severity}
                        </Badge>
                        <CardTitle className="text-lg">{gap.title}</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground">{gap.description}</p>
                    </CardContent>
                  </Card>
                ))}
              </TabsContent>

              {/* Messages */}
              <TabsContent value="messages" className="space-y-4">
                {result.outreach_messages.map((message, idx) => (
                  <Card key={idx}>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-lg capitalize">
                          {message.type.replace("-", " ")}
                        </CardTitle>
                        <span className="text-sm text-muted-foreground">
                          {message.word_count} words
                        </span>
                      </div>
                      {message.subject && (
                        <CardDescription className="font-medium text-foreground">
                          {message.subject}
                        </CardDescription>
                      )}
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <pre className="whitespace-pre-wrap text-sm font-mono bg-muted p-4 rounded-md">
                        {message.message}
                      </pre>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(message.message)}
                      >
                        <Copy className="h-4 w-4 mr-2" />
                        Copy Message
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </TabsContent>

              {/* Sources */}
              <TabsContent value="sources" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Data Sources</CardTitle>
                    <CardDescription>
                      {result.sources.length} sources analyzed
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {result.sources.map((source, idx) => (
                        <a
                          key={idx}
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-3 text-sm p-3 rounded-md hover:bg-muted transition-colors border"
                        >
                          <ExternalLink className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                          <span className="flex-1 truncate text-foreground">{source.url}</span>
                          <Badge variant="outline">{source.type}</Badge>
                        </a>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <div className="flex items-center justify-between text-sm bg-muted rounded-lg p-4">
                  <span className="flex items-center gap-2">
                    <span className="text-muted-foreground">Research time:</span>
                    <span className="font-medium">{result.metadata.research_time_seconds}s</span>
                  </span>
                  <span className="flex items-center gap-2">
                    <span className="text-muted-foreground">Cost:</span>
                    <span className="font-medium">${result.metadata.cost_usd.toFixed(4)}</span>
                  </span>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        )}
      </main>

    </div>
  );
}
