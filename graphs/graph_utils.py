def format_graph_context(func_summaries, call_graph=None, class_hierarchy=None):
    """
    Format function summaries and graph information into a readable structured input.
    """
    lines = ["You are summarizing a Python module."]

    if func_summaries:
        lines.append("Function Summaries:")
        for name, summary in func_summaries.items():
            lines.append(f"- {name}: {summary}")

    if call_graph:
        lines.append("\nCall Graph:")
        for caller, callees in call_graph.items():
            if callees:
                lines.append(f"- {caller} → {', '.join(callees)}")

    if class_hierarchy:
        lines.append("\nClass Hierarchy:")
        for cls, methods in class_hierarchy.items():
            lines.append(f"- {cls}: [{', '.join(methods)}]")

    return "\n".join(lines)
