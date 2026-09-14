#!/usr/bin/env bash
# Grade skill-craft's own operational files against the band this
# corpus declares for itself.
#
#     31 words/sentence   35 em dashes per 1000 words
#
# WHY THE TOOL'S OWN DEFAULT IS NOT USED ON THE TOOL'S OWN CORPUS.
# register_lint ships a default derived from a sample of short
# imperative skills (top of band: 5.34 dashes per 1000 words). All
# eight files here sit 2.6x-6.0x above that, so under the default this
# repo is permanently red — and a checker whose own home never passes
# is how a reader learns to discount it. That is the check-fires-on-a-
# non-defect failure, and the repair is a declared band, never a
# softened default: the default still governs every corpus that
# declares nothing, which is the population it was chosen for.
#
# THE NUMBERS, and what they are not. Derived as the worst file on
# each axis plus roughly a tenth: enforcement.md at 27.9 words/
# sentence and review-checklist.md at 32.2 dashes per 1000 words. So
# this is a CEILING WITH HEADROOM over what the corpus measures today,
# never a description of it, and drift past it fires. A band re-derived
# from the corpus each run would go green byte-identically to health.
#
# These values are the author's derivation, not an operator decision,
# and they are the first thing to change if the corpus's shape should
# move rather than be ratified. Note what they say about this corpus:
# its SENTENCES are short (15.5-27.9, inside its own prose-form
# teaching) while its EM-DASH rate is not — the axis where a skill
# corpus drifts first is the one its own SKILL.md says least about.
set -u

BAND_WORDS_PER_SENTENCE=31
BAND_EM_DASHES_PER_1000=35

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
skill="$here/../plugin/skills/skill-craft"
lint="$here/../plugin/tools/register_lint.py"

if [ ! -f "$lint" ]; then
    echo "register-check: COULD NOT VERIFY — $lint missing" >&2
    exit 2
fi

fail=0
graded=0
while IFS= read -r f; do
    graded=$((graded + 1))
    python3 "$lint" "$f" \
        --band "$BAND_WORDS_PER_SENTENCE" "$BAND_EM_DASHES_PER_1000" \
        || fail=1
done < <(find "$skill" -name '*.md' | sort)

# A run over zero files exits clean and reads as "checked and clean".
if [ "$graded" -eq 0 ]; then
    echo "register-check: COULD NOT VERIFY — no markdown under $skill" >&2
    exit 2
fi

if [ "$fail" -eq 0 ]; then
    echo "register-check: $graded file(s) inside the declared band" \
         "(${BAND_WORDS_PER_SENTENCE} w/s, ${BAND_EM_DASHES_PER_1000}/1000w)"
fi
exit "$fail"
