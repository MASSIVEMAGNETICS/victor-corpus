import pytest

from organ_connector import OrganConnector, OrganRegistrationError
from victor_corpus import VictorCorpus


def test_corpus_awakening() -> None:
    corpus = VictorCorpus(bloodline_seed="Bando_Tori_Victor_440")

    assert corpus.identity.startswith("Victor Corpus")
    assert corpus.bloodline_fingerprint is not None
    assert len(corpus.bloodline_fingerprint) == 64
    assert corpus.bloodline_seed is None
    assert "Bando_Tori_Victor_440" not in repr(corpus)


def test_corpus_identity_is_deterministic() -> None:
    first = VictorCorpus(bloodline_seed="Bando_Tori_Victor_440")
    second = VictorCorpus(bloodline_seed="Bando_Tori_Victor_440")

    assert first.identity == second.identity
    assert first.bloodline_fingerprint == second.bloodline_fingerprint


@pytest.mark.parametrize("seed", ["", "   "])
def test_corpus_rejects_blank_seed(seed: str) -> None:
    with pytest.raises(ValueError, match="cannot be blank"):
        VictorCorpus(bloodline_seed=seed)


def test_connector_is_explicit_and_bounded() -> None:
    connector = OrganConnector()
    connector.register("double", lambda value: value * 2)

    assert connector.registered_organs == ("double",)
    assert connector.invoke("double", 21) == 42

    with pytest.raises(OrganRegistrationError, match="already registered"):
        connector.register("double", lambda value: value)

    with pytest.raises(KeyError, match="unknown organ"):
        connector.invoke("missing")
