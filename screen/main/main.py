from flask import Blueprint, render_template, request
import dbcl
import datetime

main_bp = Blueprint("mnuplus_main", __name__)

@main_bp.route("/")
def main_intro():
    return render_template('main/intro.html')
