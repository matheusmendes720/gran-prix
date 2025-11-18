# 🐛 Debugging Setup - Chrome DevTools MCP & Playwright

## Overview

This document describes the debugging infrastructure setup for the Nova Corrente ML Dashboard, including Chrome DevTools MCP integration and Playwright automation for console log monitoring and active debugging feedback loops.

## Chrome DevTools MCP Setup

Based on [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp), we've configured an MCP server to enable browser automation and debugging directly from Cursor IDE.

### Installation

The Chrome DevTools MCP server is configured in `.cursor/mcp.json` and will be automatically installed when you use the MCP tools in Cursor.

### Configuration

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=false",
        "--isolated=true",
        "--viewport=1920x1080"
      ]
    }
  }
}
```

### Features Available

**DOM Inspection** (8 tools):
- `get_node` - Get DOM node information
- `list_nodes` - List DOM nodes
- `query_selector` - Query DOM elements
- `get_computed_styles` - Get computed CSS styles
- `get_accessibility_tree` - Get accessibility tree
- `get_content_quads` - Get content quad coordinates
- `describe_node` - Describe DOM node
- `focus_node` - Focus on DOM node

**Interaction Automation** (8 tools):
- `click` - Click elements
- `drag` - Drag elements
- `fill` - Fill input fields
- `fill_form` - Fill entire forms
- `handle_dialog` - Handle dialog boxes
- `hover` - Hover over elements
- `press_key` - Press keyboard keys
- `upload_file` - Upload files

**Navigation Automation** (6 tools):
- `close_page` - Close pages
- `list_pages` - List open pages
- `navigate_page` - Navigate to URLs
- `new_page` - Create new pages
- `select_page` - Select active page
- `wait_for` - Wait for conditions

**Performance** (3 tools):
- `performance_analyze_insight` - Analyze performance
- `performance_start_trace` - Start performance tracing
- `performance_stop_trace` - Stop performance tracing

**Network** (2 tools):
- `get_network_request` - Get network request details
- `list_network_requests` - List all network requests

**Debugging** (5 tools):
- `evaluate_script` - Execute JavaScript
- `get_console_message` - Get console messages
- `list_console_messages` - List all console messages
- `take_screenshot` - Take screenshots
- `take_snapshot` - Take DOM snapshots

## Usage in Cursor

### Console Log Monitoring

Use the Chrome DevTools MCP tools to monitor console logs in real-time:

```typescript
// The AI assistant can now:
// 1. Navigate to your app: navigate_page("http://localhost:3000")
// 2. Monitor console: list_console_messages()
// 3. Take snapshots: take_snapshot()
// 4. Get errors: get_console_message(filter="error")
```

### Active Debugging Feedback Loop

1. **Start Development Server**
   ```bash
   cd frontend && npm run dev
   ```

2. **Use MCP Tools in Cursor**
   - Navigate to the app using `navigate_page`
   - Monitor console logs with `list_console_messages`
   - Take snapshots when errors occur
   - Debug interactively using `evaluate_script`

3. **Fix Issues**
   - AI assistant can identify errors from console logs
   - Fix code based on error messages
   - Re-test using MCP tools

4. **Verify Fixes**
   - Monitor console for new errors
   - Check network requests
   - Verify UI behavior

## SSR Issues Fixed

### ToastContainer SSR Fix

**Issue**: `ReferenceError: document is not defined` during server-side rendering.

**Solution**: Added client-side only rendering checks:

```typescript
'use client';

const ToastContainer: React.FC = () => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // ... rest of initialization
  }, []);

  // Don't render on server side
  if (!mounted || typeof window === 'undefined') return null;
  
  // ... rest of component
};
```

### Key Changes

1. Added `'use client'` directive
2. Added `mounted` state to track client-side hydration
3. Check `typeof window === 'undefined'` before accessing `document`
4. Move `document.body` access inside component after mount check

## Playwright Integration

For automated testing and debugging, Playwright can be integrated alongside Chrome DevTools MCP:

```typescript
// Example: Monitor console logs with Playwright
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

page.on('console', msg => {
  console.log(`Browser console: ${msg.text()}`);
  if (msg.type() === 'error') {
    console.error(`Console error: ${msg.text()}`);
  }
});

await page.goto('http://localhost:3000');
```

## Debugging Workflow

### 1. Start Dev Server
```bash
cd frontend && npm run dev
```

### 2. Monitor with Chrome DevTools MCP
- Use `navigate_page` to go to `http://localhost:3000`
- Use `list_console_messages` to see all console output
- Filter errors: `get_console_message(filter="error")`

### 3. Debug Issues
- Use `take_snapshot` to capture DOM state
- Use `evaluate_script` to test fixes
- Use `take_screenshot` to visualize issues

### 4. Fix and Verify
- Fix code based on console errors
- Re-test using MCP tools
- Verify no new errors appear

## Common Issues and Solutions

### Issue: `document is not defined`
**Solution**: Add `'use client'` directive and check `typeof window !== 'undefined'`

### Issue: `window is not defined`
**Solution**: Use `useEffect` hook to access browser APIs only on client side

### Issue: Hydration mismatch
**Solution**: Ensure server and client render the same initial HTML

### Issue: Console errors not visible
**Solution**: Use Chrome DevTools MCP `list_console_messages` to capture all errors

## Best Practices

1. **Always check for browser environment**
   ```typescript
   if (typeof window === 'undefined') return null;
   ```

2. **Use `'use client'` directive** for components using browser APIs

3. **Monitor console logs** during development using MCP tools

4. **Test SSR** by disabling JavaScript in browser

5. **Use React 18+ features** like `useEffect` for client-side only code

## References

- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [npm Package](https://npmjs.org/package/chrome-devtools-mcp)
- [Next.js SSR Guide](https://nextjs.org/docs/pages/building-your-application/rendering)
- [Playwright Documentation](https://playwright.dev)

---

**Status**: ✅ Setup Complete
**Last Updated**: November 2025




















