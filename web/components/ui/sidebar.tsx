"use client";

import { cn } from "@/lib/utils";
import { Home, Target, Settings, BarChart3, CreditCard } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const navigation = [
  { name: "Overview", href: "/", icon: Home },
  { name: "Discovery", href: "/discovery", icon: Target },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Billing", href: "/billing", icon: CreditCard },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const [usage, setUsage] = useState({ api_calls: 0, limit: 1000, percentage: 0 });

  useEffect(() => {
    fetchUsage();
    // Refresh every 30 seconds
    const interval = setInterval(fetchUsage, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchUsage = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/analytics");
      const data = await response.json();
      if (data.status === "success" && data.usage) {
        setUsage(data.usage);
      }
    } catch (error) {
      // Silently fail - don't show error to user
      console.log("Failed to fetch usage:", error);
    }
  };

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-card">
      {/* Logo */}
      <div className="flex h-16 items-center border-b px-6">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center flex-shrink-0 shadow-lg">
            <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
              <circle cx="12" cy="12" r="3"/>
              <path d="M12 7v5l3.5 2"/>
            </svg>
          </div>
          <div>
            <span className="text-lg font-bold bg-gradient-to-r from-purple-600 to-purple-400 bg-clip-text text-transparent">
              Prospector
            </span>
            <p className="text-xs text-muted-foreground">AI Research</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-accent text-accent-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Usage Stats */}
      <div className="border-t p-4">
        <div className="rounded-lg bg-muted p-3 space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">API Usage</span>
            <span className="font-medium">{usage.percentage}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-background">
            <div className="h-full bg-primary transition-all" style={{ width: `${usage.percentage}%` }} />
          </div>
          <p className="text-xs text-muted-foreground">
            {usage.api_calls} / {usage.limit} requests this month
          </p>
        </div>
      </div>

      {/* User */}
      <div className="border-t p-4">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-primary" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">User</p>
            <p className="text-xs text-muted-foreground truncate">Free Plan</p>
          </div>
        </div>
      </div>
    </div>
  );
}
