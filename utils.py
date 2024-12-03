def extract_page_number(input_string):
    """
    Extracts the page number from the input string.

    Args:
        input_string (str): The string containing the page information.

    Returns:
        int: The extracted page number, or None if not found.
    """
    keyword = "_pages_"
    start_index = input_string.find(keyword)

    if start_index != -1:
        start_index += len(keyword)
        page_number = ""
        for char in input_string[start_index:]:
            if char.isdigit():
                page_number += char
            else:
                break
        return int(page_number) if page_number else None
    return None