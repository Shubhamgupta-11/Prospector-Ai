"use client";

import { useState, useEffect } from "react";
import { Search, Target, Building2, MapPin, Users, TrendingUp, Loader2, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface DiscoveredCompany {
  name: string;
  url: string;
  description?: string;
}

export default function DiscoveryPage() {
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [companies, setCompanies] = useState<DiscoveredCompany[]>([]);
  const [analytics, setAnalytics] = useState({
    total: 0,
    high_priority: 0,
    industries: 0,
    avg_score: 0
  });

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/history?limit=50");
      const data = await response.json();
      
      if (data.status === "success" && data.history) {
        // Convert research history to company format
        const companyList = data.history.map((h: any) => ({
          name: h.company_name,
          url: h.company_url,
          industry: h.industry,
          intent_score: h.intent_score,
          location: h.location || "Unknown"
        }));
        setCompanies(companyList);
        
        // Calculate stats
        const highPriority = companyList.filter((c: any) => c.intent_score >= 80).length;
        const industries = new Set(companyList.map((c: any) => c.industry).filter(Boolean)).size;
        const avgScore = companyList.length > 0 
          ? Math.round(companyList.reduce((sum: number, c: any) => sum + c.intent_score, 0) / companyList.length)
          : 0;
        
        setAnalytics({
          total: companyList.length,
          high_priority: highPriority,
          industries,
          avg_score: avgScore
        });
      }
    } catch (error) {
      console.error("Failed to fetch history:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredCompanies = companies.filter((c: any) =>
    searchQuery ? c.name.toLowerCase().includes(searchQuery.toLowerCase()) : true
  );

  const handleResearch = (url: string) => {
    window.location.href = `/?url=${encodeURIComponent(url)}`;
  };

  if (loading) {
    return (
      <div className="flex h-full flex-col bg-background">
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
                <h1 className="text-2xl font-bold">Lead Discovery</h1>
                <p className="text-sm text-muted-foreground">
                  Companies you've researched
                </p>
              </div>
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
          <div>
            <h1 className="text-2xl font-semibold">Lead Discovery</h1>
            <p className="text-sm text-muted-foreground">
              Find companies matching your ICP criteria
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-auto px-8 py-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Stats Cards */}
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Researched</CardTitle>
                <Building2 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.total}</div>
                <p className="text-xs text-muted-foreground">Companies analyzed</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">High Priority</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.high_priority}</div>
                <p className="text-xs text-muted-foreground">Score 80+</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Industries</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.industries}</div>
                <p className="text-xs text-muted-foreground">Unique sectors</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Avg Score</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{analytics.avg_score}</div>
                <p className="text-xs text-muted-foreground">ICP match quality</p>
              </CardContent>
            </Card>
          </div>

          {/* Search and Filters */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Researched Companies</CardTitle>
                  <CardDescription>Companies you've analyzed so far</CardDescription>
                </div>
                <Button variant="outline" size="sm" onClick={fetchHistory}>
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-4">
                <Input
                  placeholder="Search companies..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1"
                />
                <Button>
                  <Search className="h-4 w-4 mr-2" />
                  Search
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Companies Table */}
          <Card>
            <CardHeader>
              <CardTitle>Company List</CardTitle>
              <CardDescription>{filteredCompanies.length} companies</CardDescription>
            </CardHeader>
            <CardContent>
              {filteredCompanies.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Company</TableHead>
                      <TableHead>Industry</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead className="text-right">Score</TableHead>
                      <TableHead className="text-right">Action</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredCompanies.slice(0, 20).map((company: any, idx) => (
                      <TableRow key={idx}>
                        <TableCell className="font-medium">{company.name}</TableCell>
                        <TableCell>
                          {company.industry ? (
                            <Badge variant="outline">{company.industry}</Badge>
                          ) : (
                            <span className="text-muted-foreground text-sm">Unknown</span>
                          )}
                        </TableCell>
                        <TableCell className="text-muted-foreground">
                          {company.location && (
                            <div className="flex items-center gap-1">
                              <MapPin className="h-3 w-3" />
                              {company.location}
                            </div>
                          )}
                        </TableCell>
                        <TableCell className="text-right">
                          <span className={`font-bold ${
                            company.intent_score >= 80 ? 'text-green-600' :
                            company.intent_score >= 60 ? 'text-blue-600' :
                            company.intent_score >= 40 ? 'text-yellow-600' :
                            'text-red-600'
                          }`}>
                            {company.intent_score}
                          </span>
                        </TableCell>
                        <TableCell className="text-right">
                          <Button 
                            size="sm" 
                            variant="outline"
                            onClick={() => handleResearch(company.url)}
                          >
                            View
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <div className="text-center py-12">
                  <Building2 className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
                  <p className="text-muted-foreground mb-2">No companies researched yet</p>
                  <p className="text-sm text-muted-foreground mb-4">
                    Go to Overview and research your first company!
                  </p>
                  <Button onClick={() => window.location.href = '/'}>
                    Start Researching
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
