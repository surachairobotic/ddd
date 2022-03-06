#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"
#include "sensor_msgs/msg/point_cloud.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/point_cloud_conversion.hpp"
#include "sensor_msgs/point_cloud2_iterator.hpp"
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <cmath>

using std::placeholders::_1;

class PC_Process : public rclcpp::Node {
public:
    PC_Process()
    : Node("pc_sub")
    {
        this->pc = new sensor_msgs::msg::PointCloud();
        this->sub_pc = this->create_subscription<sensor_msgs::msg::PointCloud>(
            "/agribot/z_pc1", 10, std::bind(&PC_Process::cb_pc, this, _1));
    }

private:
    void cb_pc(const sensor_msgs::msg::PointCloud::SharedPtr msg) {
        //RCLCPP_INFO(this->get_logger(), "cb_pc");
        float min_z = msg->points[0].z;
        unsigned int indx_z = 0;
        for(unsigned int i=1; i<msg->points.size(); i++) {
            if(min_z > msg->points[i].z) {
                min_z = msg->points[i].z;
                indx_z = i;
            }
        }
        RCLCPP_INFO(this->get_logger(), "min_z= %f, indx=%d", min_z, indx_z);
    }
  
    rclcpp::Subscription<sensor_msgs::msg::PointCloud>::SharedPtr sub_pc;
    rclcpp::TimerBase::SharedPtr timer_;

    sensor_msgs::msg::PointCloud *pc;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PC_Process>());
    rclcpp::shutdown();
    return 0;
}
