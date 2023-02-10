
import spacy

import helpner.utils as ut


def test_parse_message(mocker):
    # Simple way of getting a Span
    msg = "this is a sample text"
    nlp = spacy.blank("en")
    doc = nlp(msg)
    span1 = doc[0:2]
    span1.label_ = "ARG"
    span1.start_char = 0
    span1.end_char = 1
    span2 = doc[1:]
    span1.label_ = "OPT"
    span1.start_char = 4
    span1.end_char = 6
    entities = (span1, span2)
    mocker.patch("helpner.utils._process_message", return_value=entities)
    parsed = ut.parse_message(msg)
    assert isinstance(parsed, dict)
    assert len(parsed) == 3
    assert all([i in parsed.keys() for i in ("entities", "labels", "message")])
    assert isinstance(parsed["labels"], list)
    assert len(parsed["labels"]) == 2
