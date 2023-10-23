import json

import requests

from rest_framework.exceptions import ParseError

from config.settings import BOARD_API_URL, BOARD_API_TOKEN

from fingerprints.serializers.internal.enrollment import \
    EnrollmentFingerBoardCreateSerializer


class BoardSyncService:
    def create_in_board(self, person, enrollment):
        fingers = enrollment.fingers.all()
        body = json.dumps({
            'person': person.get('board_id'),
            'fingers': EnrollmentFingerBoardCreateSerializer(fingers, many=True).data,
        })

        headers = self._generate_header()
        url = f'{BOARD_API_URL}api/biometry/fingerprints/enrollment/{person.get("status").code}/'
        response = requests.post(url, body, headers=headers, verify=False)
        if response.status_code != 201:
            raise ParseError(response.text)
        return

    def destroy_in_board(self, person):
        headers = self._generate_header()
        person_status = person.status.code
        person_id = person.board_id
        url = f'{BOARD_API_URL}api/biometry/fingerprints/destroying/{person_status}/{person_id}/'
        response = requests.delete(url, headers=headers, verify=False)
        if response.status_code != 204:
            raise ParseError(response.text)
        return

    @staticmethod
    def _generate_header():
        headers = requests.sessions.default_headers()
        headers['AuthToken'] = BOARD_API_TOKEN
        headers['Content-Type'] = 'application/json'
        return headers
