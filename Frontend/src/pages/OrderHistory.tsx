import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Package } from "lucide-react";

const OrderHistory = () => {
  const { isAuthenticated } = useAuth();

  // Mock order data
  const orders = [
    {
      id: "ORD-001",
      date: "2024-01-15",
      items: 5,
      total: 89.45,
      status: "Delivered",
    },
    {
      id: "ORD-002",
      date: "2024-01-10",
      items: 3,
      total: 45.2,
      status: "Delivered",
    },
    {
      id: "ORD-003",
      date: "2024-01-05",
      items: 8,
      total: 125.8,
      status: "Delivered",
    },
  ];

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold mb-4">Please Login</h1>
        <p className="text-gray-600 mb-8">
          You need to be logged in to view your order history.
        </p>
        <Link to="/login" className="btn-primary">
          Go to Login
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Order History</h1>

      {orders.length === 0 ? (
        <div className="text-center py-16">
          <Package size={64} className="mx-auto text-gray-300 mb-4" />
          <h2 className="text-2xl font-bold mb-4">No Orders Yet</h2>
          <p className="text-gray-600 mb-8">
            You haven't placed any orders yet. Start shopping to see your orders
            here.
          </p>
          <Link to="/products" className="btn-primary">
            Start Shopping
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div key={order.id} className="card p-6">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-4 mb-2">
                    <h3 className="text-xl font-semibold">Order {order.id}</h3>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        order.status === "Delivered"
                          ? "bg-green-100 text-green-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {order.status}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-1">
                    Placed on{" "}
                    {new Date(order.date).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </p>
                  <p className="text-gray-600">
                    {order.items} {order.items === 1 ? "item" : "items"} -
                    Total: Rs. {order.total.toFixed(0)}
                  </p>
                </div>
                <div className="flex gap-3">
                  <button className="btn-outline">View Details</button>
                  {order.status === "Delivered" && (
                    <button className="btn-secondary">Reorder</button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default OrderHistory;
