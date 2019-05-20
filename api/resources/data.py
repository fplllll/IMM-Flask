from flask_restful import reqparse, Resource
from models import retrieve_model
from models.declarative_models import WarningLog, Motor
from base.basic_base import Session
from sqlalchemy import func
from serializer.data_serializer import WarningSchema

trend_parser = reqparse.RequestParser()
trend_parser.add_argument('timeafter', location='args', required=False, type=str)
trend_parser.add_argument('timebefore', location='args', required=False, type=str)
trend_parser.add_argument('feature', location='args', required=True, type=str,
                          help='At least one feature indicator should be given, try one of [rms, max, min, thd, imbalance]'
                          )


class MotorTrend(Resource):
    def get(self, id):
        """
        Motor feature trend
        ---
        parameters:
          - in: path
            name: id
            required: true
            description: The ID of the related motor,try 1~3
            type: int
            default: 2
          - in: query
            name: feature
            required: true
            description: chose one or more of [rms, max_current, min_current, thd, imbalance,harmonics,fbrb,n_rms,p_rms,z_rms]
            type: array
            enum: ['rms', 'max_current', 'min_current', 'thd', 'imbalance','n_rms','p_rms','z_rms']

          - in: query
            name: timeafter
            required: true
            description: Start time, pattern:2016-01-01 00:00:00
            type: string
            formatter: date-time
            default: 2016-01-01 00:00:00
          - in: query
            name: timebefore
            required: true
            description: End time, pattern:2016-05-01 00:00:00
            type: string
            formatter: date-time
            """
        args = trend_parser.parse_args()
        result = retrieve_model.get_motor_trend(id, args)
        dic = {}
        for row in result:
            for key, value in row.items():
                if key == 'time':
                    dic.setdefault(key, []).append(str(value))
                else:
                    dic.setdefault(key, []).append(value)
        return dic


warning_parser = reqparse.RequestParser()
warning_parser.add_argument('isgroup', location='args', required=False, type=bool)


class MotorWarning(Resource):
    def get(self):
        """
        Motor Warning
        ---
        parameters:
          - in: query
            name: id
            required: false
            description: The ID of the related motor,try 1~3
            type: int
            default: 2
          - in: query
            name: isgroup
            required: false
            description: chose one or more of [rms, max_current, min_current, thd, imbalance,harmonics,fbrb,n_rms,p_rms,z_rms]
            type: boolean

        """
        args = warning_parser.parse_args()
        if args['isgroup']:
            data = Session.query(Motor.name, func.count(WarningLog.motor_id)). \
                join(Motor). \
                group_by(Motor.name).all()
            return data
        else:
            data = Session.query(Motor.name, WarningLog.cr_time, WarningLog.description, WarningLog.severity). \
                join(Motor). \
                order_by(WarningLog.cr_time.desc()). \
                slice(0, 7).all()
            return WarningSchema().dump(data, many=True).data
