# Version Update Procedures

## TrueNorth Extension Update Mantra

"Build Clean, Package Simple, Uninstall Old, Install Fresh"

Translation:
- Build Clean = rm -rf out && npm run compile
- Package Simple = Use basic compile script, not production config
- Uninstall Old = code --uninstall-extension truenorth.true-north-agent-system
- Install Fresh = code --install-extension *.vsix

Or the even shorter version:

"Clean → Compile → Uninstall → Install"

This ensures every version update follows the proven pattern that actually works instead of hoping VS Code will magically pick up changes! 🚀