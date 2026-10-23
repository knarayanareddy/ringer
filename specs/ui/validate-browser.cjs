#!/usr/bin/env node
/* Rendered browser checks. Install with npm ci; see TOOLING.md for headless Linux notes. */
"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium: playwrightChromium } = require("playwright-core");

const ROOT = __dirname;
const PAGES = ["index.html", "accesshold/wireframe.html", "curiolab/wireframe.html", "nexttime/wireframe.html", "harvestgrid/wireframe.html", "roomsmith/wireframe.html"];
const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 1000, reducedMotion: "no-preference" },
  { name: "mobile", width: 390, height: 844, reducedMotion: "reduce" },
];
const REPORT_ARG = process.argv.indexOf("--report");
const REPORT_PATH = REPORT_ARG >= 0 ? process.argv[REPORT_ARG + 1] : process.env.UI_BROWSER_REPORT;
const SCREENSHOT_DIR = process.env.UI_SCREENSHOT_DIR;

function packageVersion(name) {
  try {
    return require(`${name}/package.json`).version;
  } catch (_error) {
    let directory = path.dirname(require.resolve(name));
    while (directory !== path.dirname(directory)) {
      const manifest = path.join(directory, "package.json");
      if (fs.existsSync(manifest)) {
        const parsed = JSON.parse(fs.readFileSync(manifest, "utf8"));
        if (parsed.name === name) return parsed.version;
      }
      directory = path.dirname(directory);
    }
    throw new Error(`Unable to locate package manifest for ${name}`);
  }
}

async function launchBrowser() {
  if (process.env.CHROME_PATH) {
    return playwrightChromium.launch({ executablePath: process.env.CHROME_PATH, headless: true, args: ["--no-sandbox"] });
  }
  if (process.platform !== "linux") {
    throw new Error("Set CHROME_PATH to a local Chromium/Chrome executable on this platform.");
  }
  const chromiumEntry = require.resolve("@sparticuz/chromium");
  const chromiumPackage = await import(pathToFileURL(chromiumEntry).href);
  const serverlessChromium = chromiumPackage.default;
  const { inflate, setupLambdaEnvironment } = chromiumPackage;
  const chromiumRoot = path.resolve(path.dirname(chromiumEntry), "..");
  await inflate(path.join(chromiumRoot, "bin", "al2023.tar.br"));
  setupLambdaEnvironment(path.join(os.tmpdir(), "al2023", "lib"));
  serverlessChromium.setGraphicsMode = false;
  const executablePath = await serverlessChromium.executablePath();
  return playwrightChromium.launch({ executablePath, headless: true, args: serverlessChromium.args });
}

async function checkPage(context, relativePath, viewport, axeSource, screenshotDir) {
  const page = await context.newPage();
  await page.setViewportSize({ width: viewport.width, height: viewport.height });
  await page.emulateMedia({ reducedMotion: viewport.reducedMotion });
  const errors = [];
  const externalRequests = [];
  page.on("pageerror", (error) => errors.push(`pageerror: ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(`console: ${message.text()}`);
  });
  page.on("request", (request) => {
    if (/^https?:/i.test(request.url())) externalRequests.push(request.url());
  });
  const url = pathToFileURL(path.join(ROOT, relativePath)).href;
  const response = await page.goto(url, { waitUntil: "load" });
  if (response && !response.ok()) errors.push(`navigation status ${response.status()}`);
  await page.evaluate(() => document.fonts.ready);
  const structure = await page.evaluate(() => {
    const visibleControls = [...document.querySelectorAll("button, a.button")].filter((element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    });
    return {
      title: document.title,
      h1Count: document.querySelectorAll("h1").length,
      screenCount: document.querySelectorAll("section.wireframe").length,
      viewportWidth: window.innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      smallControls: visibleControls.filter((element) => {
        const rect = element.getBoundingClientRect();
        return rect.width < 43.5 || rect.height < 43.5;
      }).map((element) => ({
        text: (element.getAttribute("aria-label") || element.textContent || "").trim().replace(/\s+/g, " ").slice(0, 100),
        width: Math.round(element.getBoundingClientRect().width * 10) / 10,
        height: Math.round(element.getBoundingClientRect().height * 10) / 10,
      })),
    };
  });
  if (structure.documentWidth > structure.viewportWidth + 1) {
    errors.push(`horizontal overflow: document ${structure.documentWidth}px > viewport ${structure.viewportWidth}px`);
  }
  if (structure.h1Count !== 1) errors.push(`expected one h1, found ${structure.h1Count}`);
  if (structure.smallControls.length) errors.push(`${structure.smallControls.length} visible button(s) below 44×44 CSS px`);
  await page.addScriptTag({ content: axeSource });
  const axe = await page.evaluate(async () => {
    const result = await window.axe.run(document, {
      runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] },
    });
    return {
      violations: result.violations.map((violation) => ({
        id: violation.id,
        impact: violation.impact,
        help: violation.help,
        nodes: violation.nodes.map((node) => ({ target: node.target, failureSummary: node.failureSummary })),
      })),
      incomplete: result.incomplete.map((item) => ({
        id: item.id,
        nodes: item.nodes.map((node) => ({ target: node.target, failureSummary: node.failureSummary })),
      })),
      passes: result.passes.length,
    };
  });
  if (axe.violations.length) errors.push(`${axe.violations.length} axe rule(s) with violations`);
  if (externalRequests.length) errors.push(`${externalRequests.length} unexpected external request(s)`);
  let screenshot;
  if (screenshotDir) {
    const project = relativePath === "index.html" ? "index" : relativePath.split("/")[0];
    screenshot = path.join(screenshotDir, `${project}-${viewport.name}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });
  }
  await page.close();
  return {
    page: relativePath,
    viewport,
    ...structure,
    smallControls: structure.smallControls,
    axe,
    errors,
    externalRequests,
    screenshot: screenshot ? path.basename(screenshot) : undefined,
  };
}

(async () => {
  const axeSource = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
  if (SCREENSHOT_DIR) fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  const browser = await launchBrowser();
  const context = await browser.newContext({ deviceScaleFactor: 1 });
  const report = {
    status: "running",
    tools: {
      playwright: packageVersion("playwright-core"),
      axe: packageVersion("axe-core"),
      chromiumPackage: packageVersion("@sparticuz/chromium"),
      browser: browser.version(),
    },
    results: [],
  };
  try {
    for (const viewport of VIEWPORTS) {
      for (const relativePath of PAGES) {
        const result = await checkPage(context, relativePath, viewport, axeSource, SCREENSHOT_DIR);
        report.results.push(result);
        const label = `${relativePath} [${viewport.name}]`;
        if (result.errors.length) {
          console.error(`FAIL ${label}`);
          result.errors.forEach((error) => console.error(`  - ${error}`));
          result.axe.violations.forEach((violation) => {
            console.error(`  axe ${violation.id}: ${violation.help}`);
            violation.nodes.forEach((node) => console.error(`    ${node.target.join(" ")}: ${node.failureSummary}`));
          });
        } else {
          console.log(`PASS ${label} · ${result.axe.passes} axe rules passed · ${result.screenCount} screens`);
        }
      }
    }
  } finally {
    await context.close();
    await browser.close();
  }
  const failed = report.results.filter((result) => result.errors.length);
  report.status = failed.length ? "failed" : "passed";
  report.summary = {
    pages: PAGES.length,
    renderings: report.results.length,
    passed: report.results.length - failed.length,
    failed: failed.length,
    axeViolations: report.results.reduce((sum, result) => sum + result.axe.violations.length, 0),
  };
  if (REPORT_PATH) {
    const destination = path.resolve(ROOT, REPORT_PATH);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, `${JSON.stringify(report, null, 2)}\n`);
  }
  console.log(`${report.status.toUpperCase()}: ${report.summary.passed}/${report.summary.renderings} rendered page/viewport combinations passed`);
  if (failed.length) process.exitCode = 1;
})().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
