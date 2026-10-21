"use client";

import { useState, useEffect } from "react";
import { Activity, TrendingUp, Users, Target, Loader2 } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface Analytics {
  total_researches: number;
  avg_intent_score: number;
  high_priority_count: number;
  total_cost: number;
  total_time: number;
  top_industries: Array<{ industry: string; count: number }>;
}

interface Usage {
  api_calls: number;
  limit: number;
  percentage: number;
}

interface RecentResearch {
  company_name: string;
  industry: string;
  intent_score: number;
  timestamp: string;
}

export default function AnalyticsPage() {
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [recent, setRecent] = useState<RecentResearch[]>([]);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/analytics");
      const data = await response.json();
      
      if (data.status === "success") {
        setAnalytics(data.analytics);
        setUsage(data.usage);
        setRecent(data.recent_researches || []);
      }
    } catch (error) {
      console.error("Failed to fetch analytics:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    return 'Just now';
  };

  if (loading) {
    return (
      <div className="flex h-full flex-col bg-background">
        <header className="border-b bg-card">
          <div className="flex h-16 items-center justify-between px-8">
            <div>
              <h1 className="text-2xl font-semibold">Analytics</h1>
              <p className="text-sm text-muted-foreground">
                Track your research performance and insights
              </p>
            </div>
          </div>
        </header>
        <main className="flex-1 flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </main>
      </div>
    );
  }

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
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold">Analytics</h1>
              <p className="text-sm text-muted-foreground">
                Track your research performance and insights
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-auto px-8 py-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Key Metrics */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Researches</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics?.total_researches || 0}</div>
                <p className="text-xs text-muted-foreground">All time researches</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Avg Intent Score</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics?.avg_intent_score || 0}</div>
                <p className="text-xs text-muted-foreground">Average quality</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">High Priority Leads</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics?.high_priority_count || 0}</div>
                <p className="text-xs text-muted-foreground">Score 80+ companies</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">API Usage</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{usage?.percentage || 0}%</div>
                <p className="text-xs text-muted-foreground">
                  {usage?.api_calls || 0} / {usage?.limit || 1000} requests
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Research Activity */}
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Top Industries</CardTitle>
                <CardDescription>Most researched sectors</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {analytics?.top_industries && analytics.top_industries.length > 0 ? (
                  analytics.top_industries.map((item, idx) => {
                    const maxCount = analytics.top_industries[0]?.count || 1;
                    const percentage = (item.count / maxCount) * 100;
                    
                    return (
                      <div key={idx} className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span>{item.industry}</span>
                          <span className="font-medium">{item.count} researches</span>
                        </div>
                        <Progress value={percentage} />
                      </div>
                    );
                  })
                ) : (
                  <p className="text-sm text-muted-foreground text-center py-8">
                    No data yet. Start researching companies to see insights here.
                  </p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Research Summary</CardTitle>
                <CardDescription>Overall statistics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between border-b pb-3">
                  <span className="text-sm text-muted-foreground">Total Cost</span>
                  <span className="font-medium">${analytics?.total_cost?.toFixed(4) || '0.0000'}</span>
                </div>
                <div className="flex items-center justify-between border-b pb-3">
                  <span className="text-sm text-muted-foreground">Total Research Time</span>
                  <span className="font-medium">{analytics?.total_time || 0}s</span>
                </div>
                <div className="flex items-center justify-between border-b pb-3">
                  <span className="text-sm text-muted-foreground">Avg Time per Research</span>
                  <span className="font-medium">
                    {analytics?.total_researches 
                      ? Math.round((analytics.total_time || 0) / analytics.total_researches) 
                      : 0}s
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">High Priority Rate</span>
                  <span className="font-medium">
                    {analytics?.total_researches 
                      ? Math.round(((analytics.high_priority_count || 0) / analytics.total_researches) * 100) 
                      : 0}%
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Researches</CardTitle>
              <CardDescription>Your latest company analyses</CardDescription>
            </CardHeader>
            <CardContent>
              {recent && recent.length > 0 ? (
                <div className="space-y-4">
                  {recent.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between border-b pb-3 last:border-0">
                      <div className="flex-1">
                        <p className="font-medium">{item.company_name}</p>
                        <p className="text-sm text-muted-foreground">{item.industry || 'Unknown'}</p>
                      </div>
                      <div className="flex items-center gap-4">
                        <Badge variant={item.intent_score >= 80 ? "default" : "secondary"}>
                          Score: {item.intent_score}
                        </Badge>
                        <span className="text-sm text-muted-foreground w-24 text-right">
                          {formatTimeAgo(item.timestamp)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground text-center py-8">
                  No research history yet. Start by researching a company from the Overview page.
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
