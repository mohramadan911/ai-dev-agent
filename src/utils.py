def format_code(text):
    """Format code response for display."""
    lines = text.split('\n')
    formatted_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
            
        if in_code_block:
            formatted_lines.append(line)
            
    return '\n'.join(formatted_lines)