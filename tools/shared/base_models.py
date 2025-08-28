"""
Base models for Zen MCP tools.

This module contains the shared Pydantic models used across all tools,
extracted to avoid circular imports and promote code reuse.

Key Models:
- ToolRequest: Base request model for all tools
- WorkflowRequest: Extended request model for workflow-based tools
- ConsolidatedFindings: Model for tracking workflow progress
"""

import logging
from typing import Optional

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


# Shared field descriptions to avoid duplication
COMMON_FIELD_DESCRIPTIONS = {
    "model": "Model to use (see schema for options, 'auto' = Claude selects)",
    "temperature": "0.0=focused, 1.0=creative (tool defaults if unspecified)",
    "thinking_mode": "minimal/low/medium/high/max - depth vs speed tradeoff",
    "use_websearch": "Enable web search for docs and current info",
    "continuation_id": "Thread ID to continue conversation across tools",
    "images": "Image paths (absolute) or base64 data",
    "files": "Absolute paths to files/folders for context",
}

# Workflow-specific field descriptions
WORKFLOW_FIELD_DESCRIPTIONS = {
    "step": "Current step content and findings",
    "step_number": "Current step (starts at 1)",
    "total_steps": "Estimated total steps needed",
    "next_step_required": "Need another step? (false = adjust total_steps to match)",
    "findings": "Findings and insights from this step",
    "files_checked": "Files examined",
    "relevant_files": "Relevant files (absolute paths)",
    "relevant_context": "Involved methods/functions",
    "issues_found": "Issues with severity levels",
    "confidence": "exploring/low/medium/high/very_high/almost_certain/certain",
    "hypothesis": "Current theory",
    "backtrack_from_step": "Step to backtrack from",
    "use_assistant_model": "Use expert analysis (default: True)",
}


class ToolRequest(BaseModel):
    """
    Base request model for all Zen MCP tools.

    This model defines common fields that all tools accept, including
    model selection, temperature control, and conversation threading.
    Tool-specific request models should inherit from this class.
    """

    # Model configuration
    model: Optional[str] = Field(None, description=COMMON_FIELD_DESCRIPTIONS["model"])
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0, description=COMMON_FIELD_DESCRIPTIONS["temperature"])
    thinking_mode: Optional[str] = Field(None, description=COMMON_FIELD_DESCRIPTIONS["thinking_mode"])

    # Features
    use_websearch: Optional[bool] = Field(True, description=COMMON_FIELD_DESCRIPTIONS["use_websearch"])

    # Conversation support
    continuation_id: Optional[str] = Field(None, description=COMMON_FIELD_DESCRIPTIONS["continuation_id"])

    # Visual context
    images: Optional[list[str]] = Field(None, description=COMMON_FIELD_DESCRIPTIONS["images"])


class BaseWorkflowRequest(ToolRequest):
    """
    Minimal base request model for workflow tools.

    This provides only the essential fields that ALL workflow tools need,
    allowing for maximum flexibility in tool-specific implementations.
    """

    # Core workflow fields that ALL workflow tools need
    step: str = Field(..., description=WORKFLOW_FIELD_DESCRIPTIONS["step"])
    step_number: int = Field(..., ge=1, description=WORKFLOW_FIELD_DESCRIPTIONS["step_number"])
    total_steps: int = Field(..., ge=1, description=WORKFLOW_FIELD_DESCRIPTIONS["total_steps"])
    next_step_required: bool = Field(..., description=WORKFLOW_FIELD_DESCRIPTIONS["next_step_required"])


class WorkflowRequest(BaseWorkflowRequest):
    """
    Extended request model for workflow-based tools.

    This model extends ToolRequest with fields specific to the workflow
    pattern, where tools perform multi-step work with forced pauses between steps.

    Used by: debug, precommit, codereview, refactor, thinkdeep, analyze
    """

    # Required workflow fields
    step: str = Field(..., description=WORKFLOW_FIELD_DESCRIPTIONS["step"])
    step_number: int = Field(..., ge=1, description=WORKFLOW_FIELD_DESCRIPTIONS["step_number"])
    total_steps: int = Field(..., ge=1, description=WORKFLOW_FIELD_DESCRIPTIONS["total_steps"])
    next_step_required: bool = Field(..., description=WORKFLOW_FIELD_DESCRIPTIONS["next_step_required"])

    # Work tracking fields
    findings: str = Field(..., description=WORKFLOW_FIELD_DESCRIPTIONS["findings"])
    files_checked: list[str] = Field(default_factory=list, description=WORKFLOW_FIELD_DESCRIPTIONS["files_checked"])
    relevant_files: list[str] = Field(default_factory=list, description=WORKFLOW_FIELD_DESCRIPTIONS["relevant_files"])
    relevant_context: list[str] = Field(
        default_factory=list, description=WORKFLOW_FIELD_DESCRIPTIONS["relevant_context"]
    )
    issues_found: list[dict] = Field(default_factory=list, description=WORKFLOW_FIELD_DESCRIPTIONS["issues_found"])
    confidence: str = Field("low", description=WORKFLOW_FIELD_DESCRIPTIONS["confidence"])

    # Optional workflow fields
    hypothesis: Optional[str] = Field(None, description=WORKFLOW_FIELD_DESCRIPTIONS["hypothesis"])
    backtrack_from_step: Optional[int] = Field(
        None, ge=1, description=WORKFLOW_FIELD_DESCRIPTIONS["backtrack_from_step"]
    )
    use_assistant_model: Optional[bool] = Field(True, description=WORKFLOW_FIELD_DESCRIPTIONS["use_assistant_model"])

    @field_validator("files_checked", "relevant_files", "relevant_context", mode="before")
    @classmethod
    def convert_string_to_list(cls, v):
        """Convert string inputs to empty lists to handle malformed inputs gracefully."""
        if isinstance(v, str):
            logger.warning(f"Field received string '{v}' instead of list, converting to empty list")
            return []
        return v


class ConsolidatedFindings(BaseModel):
    """
    Model for tracking consolidated findings across workflow steps.

    This model accumulates findings, files, methods, and issues
    discovered during multi-step work. It's used by
    BaseWorkflowMixin to track progress across workflow steps.
    """

    files_checked: set[str] = Field(default_factory=set, description="All files examined across all steps")
    relevant_files: set[str] = Field(
        default_factory=set,
        description="Subset of files_checked identified as relevant for work at hand",
    )
    relevant_context: set[str] = Field(
        default_factory=set, description="All methods/functions identified during overall work"
    )
    findings: list[str] = Field(default_factory=list, description="Chronological findings from each work step")
    hypotheses: list[dict] = Field(default_factory=list, description="Evolution of hypotheses across steps")
    issues_found: list[dict] = Field(default_factory=list, description="All issues with severity levels")
    images: list[str] = Field(default_factory=list, description="Images collected during work")
    confidence: str = Field("low", description="Latest confidence level from steps")


# Tool-specific field descriptions are now declared in each tool file
# This keeps concerns separated and makes each tool self-contained
