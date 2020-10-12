from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.student import StudentModel


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('school_id',
        type=int,
        required=True,
        help="Học sinh cần school id."
    )

    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return student.json()
        return {'message': 'Không tìm thấy học sinh'}, 404

    @jwt_required()
    def post(self, name):
        if StudentModel.find_by_name(name):
            return {'message': "Học sinh với tên '{}' đã tồn tại.".format(name)}, 400
        data = Student.parser.parse_args()
        student = StudentModel(name, **data) # (name, data['name'], data['school_id'])
        try:
            student.save_to_db()
        except:
            return {'message': 'Lỗi xảy ra khi thêm học sinh.'}, 500
        return student.json(), 201

    @jwt_required()
    def delete(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            student.delete_from_db()
        return {'message': 'Đã xoá học sinh'}

class StudentList(Resource):
    def get(self):
        return {'students': list(map(lambda x: x.json(), StudentModel.query.all()))}
