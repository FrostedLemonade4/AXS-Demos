import pymupdf  # PyMuPDF
import unicodedata
from unidecode import unidecode


def extract_chapters_and_states(pdf_path):
    """
    Extracts Greek letters, converts them to Latin (with the first letters capitalized),
    and appends them as keys to the next occurrence of two adjacent capital letters.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict: A dictionary where keys are Greek letters (converted to Latin alphabet) and values are the adjacent capital letters.
    """
    chapters_dict = {}
    buffer = ""
    start_reading = False
    date = "____"
    name = []
    greek_letters = [
        "Alpha",
        "Beta",
        "Gamma",
        "Delta",
        "Epsilon",
        "Zeta",
        "Eta",
        "Theta",
        "Iota",
        "Kappa",
        "Lambda",
        "Mu",
        "Nu",
        "Xi",
        "Omicron",
        "Pi",
        "Rho",
        "Sigma",
        "Tau",
        "Upsilon",
        "Phi",
        "Chi",
        "Psi",
        "Omega",
    ]

    State_Map = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
        "D.C.": "District of Columbia",
        "DC": "District of Columbia",
    }
    # Open the PDF file
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            for char in text:
                if not start_reading:
                    if "University of Wisconsin" in buffer and not start_reading:
                        start_reading = True
                        buffer = (
                            "Alpha"  # Reset buffer to begin capturing relevant text
                        )
                    else:
                        buffer += char
                if start_reading:

                    date = buffer[-4:]
                    if not all(n.isdigit() for n in date):
                        buffer += char
                    elif "Professional Chapters of Alpha Chi Sigma" in buffer:
                        return chapters_dict
                    else:
                        # Process the buffer when it contains Greek letters and adjacent capital letters
                        if "May 1, 2022" not in buffer:
                            name = []
                            words = buffer.split()
                            for word in words:
                                if len(name) < 2 and word in greek_letters:
                                    name.append(word)
                                else:
                                    break
                            name = " ".join(name)
                            state = words[-2]
                            chapters_dict[name] = State_Map[state]
                        buffer = char  # Clear buffer after processing
                        date = "_"

    return chapters_dict


def greek_to_latin(greek_chars):
    """
    Convert Greek letters to Latin with the first letters capitalized.

    Args:
        greek_chars (list): List of Greek characters.

    Returns:
        str: The Greek letters converted to Latin.
    """
    greek_to_latin_map = {
        "\u0391": "Alpha",
        "\u0392": "Beta",
        "\u0393": "Gamma",
        "\u0394": "Delta",
        "\u0395": "Epsilon",
        "\u0396": "Zeta",
        "\u0397": "Eta",
        "\u0398": "Theta",
        "\u0399": "Iota",
        "\u039A": "Kappa",
        "\u039B": "Lambda",
        "\u039C": "Mu",
        "\u039D": "Nu",
        "\u039E": "Xi",
        "\u039F": "Omicron",
        "\u03A0": "Pi",
        "\u03A1": "Rho",
        "\u03A3": "Sigma",
        "\u03A4": "Tau",
        "\u03A5": "Upsilon",
        "\u03A6": "Phi",
        "\u03A7": "Chi",
        "\u03A8": "Psi",
        "\u03A9": "Omega",
        "\u03B1": "Alpha",
        "\u03B2": "Beta",
        "\u03B3": "Gamma",
        "\u03B4": "Delta",
        "\u03B5": "Epsilon",
        "\u03B6": "Zeta",
        "\u03B7": "Eta",
        "\u03B8": "Theta",
        "\u03B9": "Iota",
        "\u03BA": "Kappa",
        "\u03BB": "Lambda",
        "\u03BC": "Mu",
        "\u03BD": "Nu",
        "\u03BE": "Xi",
        "\u03BF": "Omicron",
        "\u03C0": "Pi",
        "\u03C1": "Rho",
        "\u03C3": "Sigma",
        "\u03C4": "Tau",
        "\u03C5": "Upsilon",
        "\u03C6": "Phi",
        "\u03C7": "Chi",
        "\u03C8": "Psi",
        "\u03C9": "Omega",
        "\u2206": "Delta",
        "\u0394": "Delta",
    }

    return " ".join([greek_to_latin_map.get(c, "Unknown") for c in greek_chars])


def extract_capital_pair(buffer):
    """
    Extract the first occurrence of two adjacent capital letters from a segment.

    Args:
        segment (str): Text segment to process.

    Returns:
        str: The adjacent capital letters, or None if not found.
    """
    if buffer.find("Washington, ") != -1:
        return "DC"
    else:
        temp = "_"
        for char in buffer:
            state = temp + char
            if all(
                c.isupper() and not unicodedata.name(c, "").startswith("GREEK")
                for c in state
            ):
                return state
            else:
                temp = char
