def filter_starting_from_alpha(lines):
    """
    Filters lines to process from the first occurrence of the word 'Alpha'.
    """
    start_processing = False
    filtered_lines = []

    for line in lines:
        if "Alpha" in line:
            start_processing = True  # Start processing from this point
        if start_processing:
            filtered_lines.append(line)

    return filtered_lines


def group_lines_until_year(lines):
    """
    Groups lines by appending until a line ends in a year (4-digit number).
    """
    grouped_lines = []
    current_line = ""

    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace

        # Skip empty lines
        if not line:
            continue

        # Append the current line fragment
        current_line += " " + line if current_line else line

        # Check if the current line ends with a year
        words = current_line.split()
        if words and words[-1].isdigit() and len(words[-1]) == 4:
            grouped_lines.append(current_line.strip())  # Add the grouped line
            current_line = ""  # Reset for the next group

    # Add any remaining line (in case the last line does not end with a year)
    if current_line:
        grouped_lines.append(current_line.strip())

    return grouped_lines


def chapter_map(pdf_path):
    State_Map = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
        "CA": "California", "CO": "Colorado", "CT": "Connecticut",
        "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
        "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
        "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan",
        "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
        "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
        "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
        "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
        "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
        "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
        "WI": "Wisconsin", "WY": "Wyoming",
        "D.C.": "District of Columbia", "DC": "District of Columbia"
    }

    # List to store chapter data
    collegiate_chapters = {}
    # Open the PDF and extract collegiate chapters
    with fitz.open(pdf_path) as doc:
        chapter_count = 0
        first = True
        for page in doc:
            text_blocks = page.get_text("blocks")
            lines = [block[4] for block in text_blocks]  # Extract text
            if first:
                lines = filter_starting_from_alpha(lines)
                lines = lines[5:]
                first = False
            lines = group_lines_until_year(lines)
            for line in lines:
                parts = line.split()
                # Look for valid lines containing state abbreviations
                if len(parts) > 2 and parts[-2] in State_Map:
                    # Increment chapter count
                    chapter_count += 1

                    # Extract chapter name based on chapter count
                    if chapter_count <= 24:
                        chapter_name = parts[0]
                    else:
                        chapter_name = " ".join(parts[:2])

                    state_abbreviation = parts[-2]
                    state_full_name = State_Map[state_abbreviation]
                    collegiate_chapters[chapter_name] = state_full_name

    return collegiate_chapters


def main(pdf_path, directory_path):
    collegiate_chapters = chapter_map(pdf_path)

    files = os.listdir(directory_path)
    year_counts = {}
    for file_name in files:
        name = file_name.replace('.', ' ')
        name = name.split()
        name = name[1:-1]
        name = " ".join(name)

        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)

        df["Year"] = pd.to_datetime(
            df['Constituent Specific Attributes Initiation Date Description'],
            format='%m/%d/%Y').dt.year
        file_year_counts = df['Year'].value_counts()
        year_counts[name] = file_year_counts

    print(collegiate_chapters)


if __name__ == "__main__":
    import fitz  # PyMuPDF
    import os
    import pandas as pd

    # Path to the list of chapters
    pdf_path = (
        "initiation_visualization\\Chapters-of-Alpha-Chi-Sigma-5-1-2022.pdf"
    )
    directory_path = r"initiation_visualization\Membership Visualization Data"

    main(pdf_path, directory_path)
