// Build an html-anime shot sheet from the command line.
// node harness/sheet-cli.mjs "<logline>" [seconds] [aspect] [script] [dialogue]
import { compileBrief } from "./compile.js";

const [logline, seconds = "8", aspect = "16:9", script = "indigo", dialogue = ""] =
  process.argv.slice(2);

if (!logline) {
  console.error('usage: node harness/sheet-cli.mjs "<logline>" [8|12|20] [16:9|9:16] [indigo|eclipse|noon|festival] ["dialogue"]');
  process.exit(2);
}

const sheet = compileBrief({ logline, seconds: Number(seconds), aspect, script, dialogue });
console.log(sheet.ok ? sheet.markdown : sheet.error);
process.exit(sheet.ok ? 0 : 1);
