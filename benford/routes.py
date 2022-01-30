import os
from os import path
from flask import current_app as app
from flask import render_template, request, flash, session, Blueprint
from .fileParser import FileParser
from .statistics import generate_benford_distribution, DistributionComparator
from werkzeug.utils import secure_filename
from .models import db, Analysis
from datetime import datetime as dt

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.files:
        if not request.files["file"]:
            return render_template('upload.html')

        f = request.files['file']
        secured_filename = path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename))
        f.save(secured_filename)

        file_parser = FileParser(secured_filename)
        file_parsed, message = file_parser.parse()

        if not file_parsed:
            os.remove(file_parser.file2analyse)
            flash(f"The '{f.filename}' file cannot be processed for some reasons: {message}")
            return render_template('upload.html')

        columns = file_parser.get_columns()

        if not columns:
            os.remove(file_parser.file2analyse)
            flash(f"The '{f.filename}' file does not contain any numerical column")
            return render_template('upload.html')

        session["uploadedFile"] = f.filename
        return render_template('selectDataset.html', uploadedFile=f.filename, columns=columns)

    return render_template('upload.html')


@home_bp.route('/selectDataset', methods=['GET', 'POST'])
def selectDataset():
    selected_col = request.form.get("selected_column")
    secured_filename = path.join(app.config["UPLOAD_FOLDER"], session.get("uploadedFile"))
    # skip_invalid_values = request.form.get("skipInvalidData")

    file_parser = FileParser(secured_filename, selected_col)
    file_parsed, message = file_parser.parse()

    if not file_parsed:
        os.remove(file_parser.file2analyse)
        flash(f"The {session.get('uploadedFile')} file cannot be processed for some reasons: {message}")
        return render_template('upload.html')

    leading_digit_distribution = file_parser.get_leading_digit_distribution()
    # os.remove(file_parser.file2analyse)
    if not leading_digit_distribution:
        flash(f"No valid elements in column")
        return render_template('upload.html')

    distribution_comparator = DistributionComparator(leading_digit_distribution,
                                                     generate_benford_distribution())
    analysis_is_valid, message = distribution_comparator.test_is_valid()
    if not analysis_is_valid:
        flash(f"Analysis may be invalid because of: {message}")

    chi_square, p_value, benford_confirmed = distribution_comparator.compare()

    newAnalysis = Analysis(filename=session.get('uploadedFile'),
                           column_name=selected_col,
                           created=dt.now(),
                           p_value=p_value,
                           chi_square=chi_square,
                           benford_confirmed=benford_confirmed,
                           observed_distribution=distribution_comparator.yObservedList,
                           expected_distribution=distribution_comparator.yExpectedList)
    db.session.add(newAnalysis)
    db.session.commit()

    return render_template('results.html', labels=distribution_comparator.xValues,
                           expectedDistribution=distribution_comparator.yExpectedList,
                           observedDistribution=distribution_comparator.yObservedList,
                           chi_square=chi_square, p_value=p_value, benford_confirmed=benford_confirmed)


@home_bp.route('/previousAnalysis', methods=['GET'])
def previousAnalysis():
    data = Analysis.query.all()
    return render_template('history.html', results=data)


@home_bp.route('/resultFromDatabase', methods=['GET'])
def resultFromDatabase():
    analysisId = request.args.get("analysisId")

    analysis = Analysis.query.filter(Analysis.id == analysisId).first()

    return render_template('results.html', labels=list(range(1, 10)),
                           expectedDistribution=analysis.expected_distribution,
                           observedDistribution=analysis.observed_distribution,
                           chi_square=analysis.chi_square, p_value=analysis.p_value,
                           benford_confirmed=analysis.benford_confirmed)
