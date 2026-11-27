-- Root module for this repository's standalone Lean build.
-- It is NOT a copy: the shared project's root module also imports other, unrelated targets.
-- Here it imports only the Banerjee–Smoot files (Main.lean imports Stages.lean and Mathlib).
-- `lean-toolchain`, `lakefile.toml` and `lake-manifest.json` are unmodified copies from the
-- shared project (Lean v4.37.0-rc1; Mathlib pinned in the manifest).
import Pipeline.BanerjeeSmoot.Main
