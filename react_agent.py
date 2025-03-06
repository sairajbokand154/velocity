from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import json
from datetime import datetime

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActionType(Enum):
    SEARCH = "search"
    ANALYZE = "analyze"
    EXECUTE = "execute"
    PLAN = "plan"
    REFINE = "refine"
    FINISH = "finish"
    ERROR_RECOVERY = "error_recovery"

@dataclass
class Thought:
    reasoning: str
    action_type: ActionType
    action_input: Dict[str, Any]
    confidence: float = 1.0
    timestamp: datetime = None

    def __post_init__(self):
        self.timestamp = datetime.now()

@dataclass
class Observation:
    result: Any
    success: bool
    error: str = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None

    def __post_init__(self):
        self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}

class ReActAgent:
    def __init__(self, max_retries: int = 3):
        self.thought_history: List[Thought] = []
        self.observation_history: List[Observation] = []
        self.max_retries = max_retries
        self.error_count = 0
        self.current_plan: List[ActionType] = []
        
    def reason(self, context: Dict[str, Any]) -> Thought:
        """
        Enhanced reasoning logic with multiple patterns and better context analysis
        """
        logger.info("Reasoning about current context...")
        
        # Get relevant history
        last_thought = self.thought_history[-1] if self.thought_history else None
        last_observation = self.observation_history[-1] if self.observation_history else None
        
        # Initial planning
        if not self.thought_history:
            self.current_plan = [
                ActionType.PLAN,
                ActionType.SEARCH,
                ActionType.ANALYZE,
                ActionType.EXECUTE,
                ActionType.FINISH
            ]
            return Thought(
                reasoning="Initial planning phase required",
                action_type=ActionType.PLAN,
                action_input={"query": context.get("initial_query", ""), "objective": context.get("objective", "")},
                confidence=0.9
            )

        # Error recovery logic
        if last_observation and not last_observation.success:
            self.error_count += 1
            if self.error_count >= self.max_retries:
                return Thought(
                    reasoning="Maximum retries exceeded. Need human intervention.",
                    action_type=ActionType.FINISH,
                    action_input={"error_summary": self._generate_error_summary()},
                    confidence=0.5
                )
            return self._generate_error_recovery_thought(last_observation)

        # Plan execution logic
        if self.current_plan:
            next_action = self.current_plan.pop(0)
            return self._generate_thought_for_action(next_action, context)

        # Default completion check
        if self._is_objective_complete(context):
            return Thought(
                reasoning="Objective appears to be completed successfully",
                action_type=ActionType.FINISH,
                action_input={"summary": self._generate_execution_summary()},
                confidence=0.95
            )

        # Default continuation
        return Thought(
            reasoning="Continuing with standard execution",
            action_type=ActionType.EXECUTE,
            action_input=self._prepare_execution_input(context),
            confidence=0.7
        )

    def _generate_error_recovery_thought(self, failed_observation: Observation) -> Thought:
        """
        Generate a thought focused on recovering from an error
        """
        error_type = self._analyze_error_type(failed_observation.error)
        recovery_strategy = self._determine_recovery_strategy(error_type)
        
        return Thought(
            reasoning=f"Attempting to recover from error: {error_type}",
            action_type=ActionType.ERROR_RECOVERY,
            action_input={
                "error_type": error_type,
                "recovery_strategy": recovery_strategy,
                "previous_action": failed_observation.metadata.get("action_type")
            },
            confidence=0.6
        )

    def _analyze_error_type(self, error: str) -> str:
        """
        Analyze the type of error encountered
        """
        if "permission" in error.lower():
            return "permission_error"
        if "not found" in error.lower():
            return "not_found_error"
        if "timeout" in error.lower():
            return "timeout_error"
        return "unknown_error"

    def _determine_recovery_strategy(self, error_type: str) -> Dict[str, Any]:
        """
        Determine appropriate recovery strategy based on error type
        """
        strategies = {
            "permission_error": {"action": "escalate_permissions", "retry_count": 1},
            "not_found_error": {"action": "search_alternative", "retry_count": 2},
            "timeout_error": {"action": "increase_timeout", "retry_count": 1},
            "unknown_error": {"action": "retry_with_logging", "retry_count": 1}
        }
        return strategies.get(error_type, {"action": "retry_basic", "retry_count": 1})

    def act(self, thought: Thought) -> Observation:
        """
        Enhanced action execution with better error handling and logging
        """
        logger.info(f"Executing action: {thought.action_type} with confidence {thought.confidence}")
        
        try:
            result = None
            metadata = {
                "action_type": thought.action_type,
                "confidence": thought.confidence,
                "timestamp": datetime.now().isoformat()
            }
            
            if thought.action_type == ActionType.SEARCH:
                result = self._perform_search(thought.action_input)
            elif thought.action_type == ActionType.ANALYZE:
                result = self._analyze_data(thought.action_input)
            elif thought.action_type == ActionType.EXECUTE:
                result = self._execute_action(thought.action_input)
            elif thought.action_type == ActionType.PLAN:
                result = self._create_execution_plan(thought.action_input)
            elif thought.action_type == ActionType.REFINE:
                result = self._refine_results(thought.action_input)
            elif thought.action_type == ActionType.ERROR_RECOVERY:
                result = self._handle_error_recovery(thought.action_input)
            elif thought.action_type == ActionType.FINISH:
                result = self._finalize_execution(thought.action_input)
            
            return Observation(
                result=result,
                success=True,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Action failed: {str(e)}", exc_info=True)
            return Observation(
                result=None,
                success=False,
                error=str(e),
                metadata={
                    "action_type": thought.action_type,
                    "error_timestamp": datetime.now().isoformat(),
                    "error_type": type(e).__name__
                }
            )

    def _perform_search(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement search functionality with proper error handling
        """
        query = input_data.get("query", "")
        search_type = input_data.get("search_type", "general")
        
        # Implement actual search logic here
        results = {
            "query": query,
            "search_type": search_type,
            "results": [
                {"title": "Sample Result 1", "relevance": 0.9},
                {"title": "Sample Result 2", "relevance": 0.7}
            ],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "result_count": 2
            }
        }
        
        return results

    def _analyze_data(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement data analysis with metrics and insights
        """
        data = input_data.get("data", {})
        analysis_type = input_data.get("analysis_type", "general")
        
        # Implement actual analysis logic here
        analysis_results = {
            "insights": ["Insight 1", "Insight 2"],
            "metrics": {"relevance": 0.85, "confidence": 0.9},
            "recommendations": ["Recommendation 1", "Recommendation 2"]
        }
        
        return analysis_results

    def _execute_action(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement action execution with validation and monitoring
        """
        action_params = input_data.get("params", {})
        validation_result = self._validate_action_params(action_params)
        
        if not validation_result["valid"]:
            raise ValueError(f"Invalid action parameters: {validation_result['errors']}")
        
        # Implement actual execution logic here
        execution_result = {
            "status": "completed",
            "outputs": {"key": "value"},
            "metrics": {"duration": 0.5, "success_rate": 1.0}
        }
        
        return execution_result

    def _validate_action_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate action parameters before execution
        """
        errors = []
        required_params = ["action_type", "target"]
        
        for param in required_params:
            if param not in params:
                errors.append(f"Missing required parameter: {param}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def _create_execution_plan(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a detailed execution plan
        """
        objective = input_data.get("objective", "")
        constraints = input_data.get("constraints", [])
        
        plan = {
            "steps": [
                {"action": ActionType.SEARCH, "purpose": "Gather information"},
                {"action": ActionType.ANALYZE, "purpose": "Process findings"},
                {"action": ActionType.EXECUTE, "purpose": "Implement solution"}
            ],
            "estimated_steps": 3,
            "success_criteria": ["Criteria 1", "Criteria 2"]
        }
        
        return plan

    def _is_objective_complete(self, context: Dict[str, Any]) -> bool:
        """
        Check if the current objective has been completed
        """
        if not self.observation_history:
            return False
            
        last_observation = self.observation_history[-1]
        success_criteria = context.get("success_criteria", [])
        
        if not success_criteria:
            return last_observation.success
            
        # Implement actual completion check logic here
        return last_observation.success and all(
            self._check_criterion(criterion, last_observation.result)
            for criterion in success_criteria
        )

    def _check_criterion(self, criterion: str, result: Any) -> bool:
        """
        Check if a specific success criterion has been met
        """
        # Implement actual criterion checking logic here
        return True

    def _generate_execution_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the execution history
        """
        return {
            "total_steps": len(self.thought_history),
            "success_rate": sum(1 for obs in self.observation_history if obs.success) / len(self.observation_history) if self.observation_history else 0,
            "error_count": self.error_count,
            "final_state": "completed" if self._is_objective_complete({}) else "incomplete"
        }

    def run(self, initial_context: Dict[str, Any], max_steps: int = 10) -> List[Observation]:
        """
        Enhanced run loop with better state management and logging
        """
        context = initial_context.copy()
        step = 0
        
        logger.info(f"Starting ReAct loop with context: {json.dumps(context, default=str)}")
        
        while step < max_steps:
            # Reasoning phase
            thought = self.reason(context)
            self.thought_history.append(thought)
            logger.info(f"Step {step + 1} - Thought: {thought.reasoning}")
            
            # Acting phase
            observation = self.act(thought)
            self.observation_history.append(observation)
            logger.info(f"Step {step + 1} - Observation: {observation}")
            
            # Update context with new observation and metadata
            context.update({
                "last_observation": observation,
                "last_thought": thought,
                "step": step,
                "history_summary": self._generate_execution_summary()
            })
            
            # Check completion conditions
            if thought.action_type == ActionType.FINISH or not observation.success:
                if not observation.success:
                    logger.warning(f"Loop terminated due to failure: {observation.error}")
                else:
                    logger.info("Loop completed successfully")
                break
                
            step += 1
            
        return self.observation_history

if __name__ == "__main__":
    agent = ReActAgent()
    initial_context = {
        "initial_query": "Sample task to demonstrate ReAct loop",
        "objective": "Demonstrate the ReAct loop functionality",
        "success_criteria": ["Must complete all steps", "Must handle errors appropriately"]
    }
    results = agent.run(initial_context)
    print("Final results:", json.dumps(results, default=str, indent=2)) 
