import json
from urllib.parse import unquote
from scenarios.models import Scenarios
from scenarios.serializers import ScenariosSerializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


class MypageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 10
    max_page_size = 100


class ScenariosViewSet(viewsets.ModelViewSet):
    queryset = Scenarios.objects.all().order_by('name')
    serializer_class = ScenariosSerializers
    pagination_class = MypageNumberPagination


# 筛选场景信息
class FilterScenariosViewSet(viewsets.ModelViewSet):
    queryset = Scenarios.objects.all()
    serializer_class = ScenariosSerializers
    pagination_class = MypageNumberPagination

    def get_queryset(self):
        # 获取原始的查询集
        queryset = super().get_queryset()

        # 尝试从查询字符串中获取formInlines参数
        form_inlines_param = self.request.query_params.get('formInlines', None)

        # 如果formInlines参数存在，则解码并解析为Python字典
        if form_inlines_param:
            try:
                form_inlines_data = json.loads(unquote(form_inlines_param))

                # 从字典中提取需要的过滤参数
                types_param = form_inlines_data.get('types', None)
                lines_param = form_inlines_data.get('lines', None)
                vehs_per_hour_param = form_inlines_data.get('vehsPerHour', None)
                permeability_param = form_inlines_data.get('permeability',None)

                # 根据参数过滤查询集
                if types_param is not None:
                    queryset = queryset.filter(types=types_param)
                if lines_param is not None:
                    queryset = queryset.filter(lines=lines_param)
                if vehs_per_hour_param is not None:
                    queryset = queryset.filter(vehsPerHour=vehs_per_hour_param)
                if permeability_param is not None:
                    queryset = queryset.filter(permeability=permeability_param)

            except json.JSONDecodeError:
                # 如果解码失败，则不应用任何过滤条件，或可以记录错误
                pass

                # 返回过滤后的查询集
        return queryset

