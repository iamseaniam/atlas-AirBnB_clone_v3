#!/usr/bin/python3
"""Handles RESTFul API actions for Review objects"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if storage.get("User", request.json['user_id']) is None:
        abort(404)
    if 'text' not in request.json:
        abort(400, "Missing text")
    review = Review(place_id=place_id, **request.json)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
