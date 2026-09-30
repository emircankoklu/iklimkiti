from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class GameResult:
    passed: bool
    score: int
    correct_count: int = 0
    total_questions: int = 0
    message: str = ''


class BaseGameEngine:
    """Genişletilebilir oyun motoru. TODO: skor, süre, kullanıcı ilerlemesi, oyun oturumları."""

    def validate_configuration(self, configuration: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(configuration, dict):
            raise ValueError('Oyun konfigürasyonu bir dict olmalıdır.')
        return configuration

    def evaluate(self, game, answers: dict[str, Any]) -> GameResult:
        raise NotImplementedError


class MultipleChoiceGameEngine(BaseGameEngine):
    def validate_configuration(self, configuration):
        config = super().validate_configuration(configuration)
        questions = config.get('questions', [])
        if not isinstance(questions, list) or not questions:
            raise ValueError('Çoktan seçmeli oyunda en az bir soru bulunmalıdır.')
        for question in questions:
            if 'correct_option' not in question or 'options' not in question:
                raise ValueError('Soru yapısı eksik.')
        return config

    def evaluate(self, game, answers):
        config = self.validate_configuration(game.configuration_json)
        questions = config.get('questions', [])
        correct = 0
        total = len(questions)
        for q in questions:
            choice = answers.get(q.get('id'))
            if choice == q.get('correct_option'):
                correct += 1
        passed = (correct / total) >= config.get('completion_threshold', 0.6) if total else False
        score = round((correct / total) * 100) if total else 0
        return GameResult(
            passed=passed,
            score=score,
            correct_count=correct,
            total_questions=total,
            message='Oyun tamamlandı.' if passed else 'Daha fazla tekrar deneyebilirsiniz.',
        )


class TrueFalseGameEngine(BaseGameEngine):
    def validate_configuration(self, configuration):
        config = super().validate_configuration(configuration)
        questions = config.get('questions', [])
        if not questions:
            raise ValueError('Doğru/Yanlış oyununun soruları bulunmalıdır.')
        return config

    def evaluate(self, game, answers):
        config = self.validate_configuration(game.configuration_json)
        questions = config.get('questions', [])
        total = len(questions)
        correct = 0
        for q in questions:
            if answers.get(q.get('id')) == q.get('correct_answer'):
                correct += 1
        score = round((correct / total) * 100) if total else 0
        threshold = config.get('completion_threshold', 0.6)
        return GameResult(
            passed=score >= threshold * 100,
            score=score,
            correct_count=correct,
            total_questions=total,
            message='Oyun tamamlandı.' if correct >= threshold * total else 'Kalan soruları tekrar çözün.',
        )


class GameRegistry:
    def __init__(self):
        self._engines = {
            'multiple_choice': MultipleChoiceGameEngine(),
            'true_false': TrueFalseGameEngine(),
        }

    def register(self, key: str, engine: BaseGameEngine):
        self._engines[key] = engine

    def get(self, key: str):
        if key not in self._engines:
            raise ValueError(f'Oyun türü bulunamadı: {key}')
        return self._engines[key]
