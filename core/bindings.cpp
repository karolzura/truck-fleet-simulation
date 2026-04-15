#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "include/RouteEngine.h"

namespace py = pybind11;

PYBIND11_MODULE(simulation_engine, m) {
    m.doc() = "Fleet routing engine";

    py::class_<Destination>(m, "Destination")
        .def_readonly("name",        &Destination::name)
        .def_readonly("order_id",    &Destination::order_id)
        .def_readonly("x",           &Destination::x)
        .def_readonly("y",           &Destination::y)
        .def_readonly("priority",    &Destination::priority)
        .def_readonly("deadline_ts", &Destination::deadline_ts)
        .def_readonly("visited",     &Destination::visited);

    py::class_<RouteEngine>(m, "RouteEngine")
        .def(py::init<>())
        .def("add_order",       &RouteEngine::addOrder)
        .def("remove_order",    &RouteEngine::removeOrder)
        .def("get_next_target", &RouteEngine::getNextTarget)
        .def("get_nearest_target", &RouteEngine::getNearestTarget)
        .def("assign_order",    &RouteEngine::assignOrder)
        .def("has_orders",      &RouteEngine::hasOrders)
        .def("pending_count",   &RouteEngine::pendingCount);
}