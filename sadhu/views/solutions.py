from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   url_for)
from flask_login import current_user, login_required

from pygments.lexers import get_lexer_for_filename
from pygments import highlight
from pygments.formatters import HtmlFormatter

from sadhu import acl
from sadhu import forms
from sadhu import models


module = Blueprint('solutions',
                   __name__,
                   url_prefix='/solutions',
                   )


@module.route('/')
@login_required
def index():
    solutions = models.Solution.objects(
            owner=current_user._get_current_object()).order_by('-id')
    return render_template('/solutions/index.html',
                           solutions=solutions,
                           )


@module.route('/<solution_id>/')
@login_required
def view(solution_id):
    solution = models.Solution.objects(
            id=solution_id,
            owner=current_user._get_current_object(),
            ).first()
    challenge = solution.challenge

    code = solution.code.read().decode()

    lexer = get_lexer_for_filename(solution.code.filename)

    formatter = HtmlFormatter(linenos=True)
    formated_code = highlight(code, lexer, formatter)
    style = formatter.get_style_defs('.highlight')

    return render_template('/solutions/view.html',
                           solution=solution,
                           challenge=challenge,
                           formated_code=formated_code,
                           style=style)

