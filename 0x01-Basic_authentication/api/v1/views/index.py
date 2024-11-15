#!/usr/bin/env python3
"""Module containing API status and error handling views."""


from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_api_status() -> str:
    """
    GET /api/v1/status
    Returns:
        JSON response indicating the API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def get_object_stats() -> str:
    """
    GET /api/v1/stats
    Returns:
        JSON response with the count of objects.
    """
    object_counts = {"users": User.count()}
    return jsonify(object_counts)


@app_views.route('/unauthorized/', strict_slashes=False)
def handle_unauthorized() -> None:
    """
    GET /api/v1/unauthorized
    Raises:
        401 Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def handle_forbidden() -> None:
    """
    GET /api/v1/forbidden
    Raises:
        403 Forbidden error.
    """
    abort(403)
