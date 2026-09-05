# Repository Instructions

## Topic Pack changes

Before creating or modifying a Topic Pack, read `docs/topic_pack_workflow.md` completely.

- Start every new Topic with `rubric_manager.py add-topic`; do not assemble an unmanaged scaffold manually.
- Keep the Topic in `draft / human_review_required` until a person reviews the README and source JSON.
- Record approval with `rubric_manager.py approve-topic --reviewer <reviewer_id>`.
- Do not bypass the approval/hash gate by editing generated banks directly.
- Run the full `validate-topic-pack-release --all` integration gate before commit or push.
- Treat `docs/topic_pack_workflow.md` as the human procedure and `scripts/topic_pack_workflow_controller.py` plus validators as the executable contract.
