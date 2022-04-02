import pytest

from app.adapters import slack


def test_verify_a_valid_signature():
    # signature created using "signing-secret" as signing secret
    sig = "v0=a035e098f1b14e7b9303e2c061d48b85a52499d17bcbe33940a846e888e35ba4"
    ts = "1595524130"

    # request body and headers coming from Slack webhooks
    body = (
        "token=xxx&team_id=T02RX18RT&team_domain=zmoog&channel_id=DN95R50BA"
        "&channel_name=directmessage&user_id=U02RX18RV&user_name=zmoog&"
        "command=%2Frefurbished&text=it+mac&response_url=https%3A%2F%"
        "2Fhooks.slack.com%2Fcommands%2FT02RX18RT%2F1287752509456"
        "%2FRvnHleL1XCLxuMU2zGDGRbtT&trigger_id="
        "1270097955124.2881042877.121a0b3a9cf1313830907fcdde478152"
    )
    headers = {
        "X-Slack-Signature": sig,
        "X-Slack-Request-Timestamp": ts,
    }

    slack.verify_signature(body, headers)


def test_verify_an_invalid_signature():
    # signature created using "signing-secret" as signing secret
    sig = "v0=deadbeeddeadbeeddeadbeeddeadbeeddeadbeeddeadbeeddeadbeeddeadbeed"
    ts = "1595524130"

    # request body and headers coming from Slack webhooks
    body = (
        "token=xxx&team_id=T02RX18RT&team_domain=zmoog&channel_id=DN95R50BA"
        "&channel_name=directmessage&user_id=U02RX18RV&user_name=zmoog&command"
        "=%2Frefurbished&text=it+mac&response_url=https%3A%2F%2F"
        "hooks.slack.com%2Fcommands%2FT02RX18RT%2F1287752509456%2F"
        "RvnHleL1XCLxuMU2zGDGRbtT&trigger_id=1270097955124.2881042877."
        "121a0b3a9cf1313830907fcdde478152&this_extra_parameter_makes_different"
        "%2Ftrue"
    )
    headers = {
        "X-Slack-Signature": sig,
        "X-Slack-Request-Timestamp": ts,
    }

    with pytest.raises(slack.InvalidSignature):
        slack.verify_signature(body, headers)
