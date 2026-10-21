"use client";

import { useState, useEffect } from "react";
import { Key, Save, Eye, EyeOff, CheckCircle2, Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface APIStatus {
  configured: boolean;
  key_preview: string;
}

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [apiKeys, setApiKeys] = useState<Record<string, APIStatus>>({});
  const [settings, setSettings] = useState({
    research_depth: "standard",
    discovery_limit: 10,
    email: "user@example.com"
  });
  const [message, setMessage] = useState<{ type: string; text: string } | null>(null);
  
  const [showGemini, setShowGemini] = useState(false);
  const [showTavily, setShowTavily] = useState(false);
  const [showSerp, setShowSerp] = useState(false);
  const [showBrave, setShowBrave] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/settings");
      const data = await response.json();
      
      if (data.status === "success") {
        setApiKeys(data.api_keys);
        setSettings(data.settings);
      }
    } catch (error) {
      console.error("Failed to fetch settings:", error);
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    setMessage(null);
    
    try {
      const response = await fetch("http://localhost:8000/api/v1/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings)
      });
      
      const data = await response.json();
      
      if (data.status === "success") {
        setMessage({ type: "success", text: "Settings saved successfully" });
      } else {
        setMessage({ type: "error", text: "Failed to save settings" });
      }
    } catch (error) {
      setMessage({ type: "error", text: "Failed to save settings" });
    } finally {
      setSaving(false);
    }
  };

  const testAPI = async (provider: string) => {
    setMessage({ type: "info", text: `Testing ${provider}...` });
    
    try {
      const response = await fetch("http://localhost:8000/api/v1/settings/test-api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider })
      });
      
      const data = await response.json();
      
      if (data.status === "success") {
        setMessage({ type: "success", text: `${provider} connected successfully!` });
      } else {
        setMessage({ type: "error", text: data.message || "Test failed" });
      }
    } catch (error) {
      setMessage({ type: "error", text: "Connection test failed" });
    }
  };

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
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
              <h1 className="text-2xl font-bold">Settings</h1>
              <p className="text-sm text-muted-foreground">
                Manage your API keys and preferences
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-auto px-8 py-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {/* Message */}
          {message && (
            <div className={`flex items-center gap-2 p-4 rounded-md ${
              message.type === "success" ? "bg-green-50 text-green-800 border border-green-200" :
              message.type === "error" ? "bg-red-50 text-red-800 border border-red-200" :
              "bg-blue-50 text-blue-800 border border-blue-200"
            }`}>
              {message.type === "success" && <CheckCircle2 className="h-4 w-4" />}
              {message.type === "error" && <AlertCircle className="h-4 w-4" />}
              <span className="text-sm">{message.text}</span>
            </div>
          )}

          {/* API Keys Section */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>API Configuration</CardTitle>
                  <CardDescription>Manage your API keys for AI and search services</CardDescription>
                </div>
                <Key className="h-5 w-5 text-muted-foreground" />
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Google Gemini API */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Google Gemini API Key</label>
                  {apiKeys.gemini?.configured ? (
                    <Badge variant="default" className="bg-green-500">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Connected
                    </Badge>
                  ) : (
                    <Badge variant="secondary">Not Configured</Badge>
                  )}
                </div>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      type={showGemini ? "text" : "password"}
                      value={apiKeys.gemini?.key_preview || ""}
                      readOnly
                      className="pr-10"
                    />
                    <button
                      onClick={() => setShowGemini(!showGemini)}
                      className="absolute right-3 top-1/2 -translate-y-1/2"
                    >
                      {showGemini ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </button>
                  </div>
                  <Button variant="outline" onClick={() => testAPI("gemini")}>Test</Button>
                </div>
                <p className="text-xs text-muted-foreground">
                  Free tier: 1,500 requests/day. Used for all AI analysis and content generation.
                </p>
              </div>

              {/* Tavily Search API */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Tavily Search API Key</label>
                  {apiKeys.tavily?.configured ? (
                    <Badge variant="default" className="bg-green-500">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Connected
                    </Badge>
                  ) : (
                    <Badge variant="secondary">Not Configured</Badge>
                  )}
                </div>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      type={showTavily ? "text" : "password"}
                      value={apiKeys.tavily?.key_preview || ""}
                      readOnly
                      className="pr-10"
                    />
                    <button
                      onClick={() => setShowTavily(!showTavily)}
                      className="absolute right-3 top-1/2 -translate-y-1/2"
                    >
                      {showTavily ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </button>
                  </div>
                  <Button variant="outline" onClick={() => testAPI("tavily")}>Test</Button>
                </div>
                <p className="text-xs text-muted-foreground">
                  Primary search provider for web research and company discovery.
                </p>
              </div>

              {/* SerpAPI (Optional) */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">SerpAPI Key (Optional)</label>
                  {apiKeys.serpapi?.configured ? (
                    <Badge variant="default" className="bg-green-500">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Connected
                    </Badge>
                  ) : (
                    <Badge variant="secondary">Optional</Badge>
                  )}
                </div>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      type={showSerp ? "text" : "password"}
                      value={apiKeys.serpapi?.key_preview || ""}
                      placeholder="Not configured"
                      readOnly
                      className="pr-10"
                    />
                    <button
                      onClick={() => setShowSerp(!showSerp)}
                      className="absolute right-3 top-1/2 -translate-y-1/2"
                    >
                      {showSerp ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </button>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">
                  Fallback search provider for higher availability.
                </p>
              </div>

              {/* Brave Search (Optional) */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Brave Search API Key (Optional)</label>
                  {apiKeys.brave?.configured ? (
                    <Badge variant="default" className="bg-green-500">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Connected
                    </Badge>
                  ) : (
                    <Badge variant="secondary">Optional</Badge>
                  )}
                </div>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      type={showBrave ? "text" : "password"}
                      value={apiKeys.brave?.key_preview || ""}
                      placeholder="Not configured"
                      readOnly
                      className="pr-10"
                    />
                    <button
                      onClick={() => setShowBrave(!showBrave)}
                      className="absolute right-3 top-1/2 -translate-y-1/2"
                    >
                      {showBrave ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </button>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">
                  Additional search provider for backup and redundancy.
                </p>
              </div>
              
              <p className="text-xs text-muted-foreground pt-4">
                Note: API keys are stored in your .env file. To update them, edit the .env file directly.
              </p>
            </CardContent>
          </Card>

          {/* Preferences */}
          <Card>
            <CardHeader>
              <CardTitle>Research Preferences</CardTitle>
              <CardDescription>Configure default research behavior</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Default Research Depth</label>
                <select 
                  className="w-full h-10 px-3 rounded-md border border-input bg-background"
                  value={settings.research_depth}
                  onChange={(e) => setSettings({...settings, research_depth: e.target.value})}
                >
                  <option value="quick">Quick (30 seconds)</option>
                  <option value="standard">Standard (60 seconds)</option>
                  <option value="deep">Deep (2-3 minutes)</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Discovery Results Limit</label>
                <select 
                  className="w-full h-10 px-3 rounded-md border border-input bg-background"
                  value={settings.discovery_limit}
                  onChange={(e) => setSettings({...settings, discovery_limit: parseInt(e.target.value)})}
                >
                  <option value="5">5 companies</option>
                  <option value="10">10 companies</option>
                  <option value="20">20 companies</option>
                  <option value="50">50 companies</option>
                </select>
              </div>

              <div className="pt-4">
                <Button onClick={saveSettings} disabled={saving}>
                  {saving ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="h-4 w-4 mr-2" />
                      Save Preferences
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Account */}
          <Card>
            <CardHeader>
              <CardTitle>Account Information</CardTitle>
              <CardDescription>Your account details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Email</label>
                <Input 
                  type="email" 
                  value={settings.email}
                  onChange={(e) => setSettings({...settings, email: e.target.value})}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Plan</label>
                <div className="flex items-center gap-2">
                  <Input value="Free Tier" readOnly />
                  <Button variant="outline">Upgrade</Button>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Member Since</label>
                <Input value="October 2026" readOnly />
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
