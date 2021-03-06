import math
import copy
from functools import reduce


def statement(invoice: dict, plays: dict) -> str:

    return renderPlainText(createStatementData(invoice, plays))


def createStatementData(invoice, plays):
    result = dict()
    result["customer"] = invoice["customer"]
    result["performances"] = [
        enrichPerformance(perf, plays) for perf in invoice["performances"]
    ]
    result["total_amount"] = totalAmount(result)
    result["total_volume_credits"] = totalVolumeCredits(result)
    return result


def enrichPerformance(aPerformance, plays):
    result = copy.copy(aPerformance)
    result["play"] = playFor(result, plays)
    result["amount"] = amountFor(result)
    result["volume_credits"] = volumeCreditsFor(result)
    return result


def renderPlainText(data):
    result = f'청구 내역 (고객명: {data["customer"]})\n'
    for perf in data["performances"]:
        # 청구 내역 출력
        result += (
            f'\t{perf["play"]["name"]}: ${usd(perf["amount"])} ({perf["audience"]}석)\n'
        )
    result += f"총액: ${usd(totalAmount(data))}\n"
    result += f"적립 포인트: {totalVolumeCredits(data)}점"
    return result


def totalAmount(data):
    return reduce(lambda result, perf: result + perf["amount"], data["performances"], 0)


def totalVolumeCredits(data):
    return reduce(
        lambda result, perf: result + perf["volume_credits"], data["performances"], 0
    )


def usd(aNumber):
    return format(aNumber / 100, ",")


def volumeCreditsFor(aPerformance):
    result = 0
    result += max(aPerformance["audience"] - 30, 0)
    if aPerformance["play"]["type"] == "comedy":
        result += math.floor(aPerformance["audience"] / 5)
    return result


def playFor(aPerformance, plays):
    return plays[aPerformance["playID"]]


def amountFor(aPerformance):
    result = 0
    if aPerformance["play"]["type"] == "tragedy":
        result = 40000
        if aPerformance["audience"] > 30:
            result += 1000 * (aPerformance["audience"] - 30)
    elif aPerformance["play"]["type"] == "comedy":
        result = 30000
        if aPerformance["audience"] > 20:
            result += 10000 + 500 * (aPerformance["audience"] - 20)
        result += 300 * aPerformance["audience"]
    else:
        raise Exception(f'알 수 없는 장르: {aPerformance["play"]["type"]}')
    return result