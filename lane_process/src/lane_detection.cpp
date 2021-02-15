#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "sensor_msgs/point_cloud_conversion.hpp"
#include "sensor_msgs/point_cloud2_iterator.hpp"
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>

using std::placeholders::_1;

class LaneDetection : public rclcpp::Node
{
public:
  LaneDetection()
  : Node("pc_sub"), b_run(false)
  {
    this->pc = new sensor_msgs::msg::PointCloud();
    this->pc2 = new sensor_msgs::msg::PointCloud2();
    this->qBase = new tf2::Quaternion(-0.6123724,0.6123724,-0.3535534,0.3535534);
    this->rot = new tf2::Matrix3x3(*qBase);
    publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud2>("/agribot/pc2", 10);
    subscription_ = this->create_subscription<sensor_msgs::msg::PointCloud2>(
      "/agribot/camera/rs_front/points", 10, std::bind(&LaneDetection::pc_cb, this, _1));
    timer_ = this->create_wall_timer(std::chrono::milliseconds(50), 
                                     std::bind(&LaneDetection::timer_callback, this));
  }

private:
  void pc_cb(const sensor_msgs::msg::PointCloud2::SharedPtr msg)
  {
    //RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->header.frame_id.c_str());
    if(!b_run) {
      //RCLCPP_INFO(this->get_logger(), "H,W : %d, %d", this->pc2->height, this->pc2->width);
      this->pc2->header = msg->header;
      this->pc2->height = msg->height;
      this->pc2->width = msg->width;
      this->pc2->fields = msg->fields;
      this->pc2->is_bigendian = msg->is_bigendian;
      this->pc2->point_step = msg->point_step;
      this->pc2->row_step = msg->row_step;
      this->pc2->data = msg->data;
      this->pc2->is_dense = msg->is_dense;
      b_run = true;
    }
  }
  
  void timer_callback() {
    /*
    RCLCPP_INFO(this->get_logger(), "timer : start");
    RCLCPP_INFO(this->get_logger(), "%lf, %lf, %lf", this->matrix2base->getRow(0).x(), this->matrix2base->getRow(0).y(), this->matrix2base->getRow(0).z());
    RCLCPP_INFO(this->get_logger(), "%lf, %lf, %lf", this->matrix2base->getRow(1).x(), this->matrix2base->getRow(1).y(), this->matrix2base->getRow(1).z());
    RCLCPP_INFO(this->get_logger(), "%lf, %lf, %lf", this->matrix2base->getRow(2).x(), this->matrix2base->getRow(2).y(), this->matrix2base->getRow(2).z());
    RCLCPP_INFO(this->get_logger(), "timer : end");
    */
    if(b_run) {
      //pc2_to_pc();
      pc2_process();
      b_run = false;
    }
  }
  
  void pc2_process(void) {
    sensor_msgs::PointCloud2Modifier pcd_modifier(*(this->pc2));
    pcd_modifier.setPointCloud2FieldsByString(2,"xyz","rgb");
    
    sensor_msgs::PointCloud2Iterator<float> iter_x(*(this->pc2), "x");
    sensor_msgs::PointCloud2Iterator<float> iter_y(*(this->pc2), "y");
    sensor_msgs::PointCloud2Iterator<float> iter_z(*(this->pc2), "z");
    sensor_msgs::PointCloud2Iterator<uint8_t> iter_r(*(this->pc2), "r");
    sensor_msgs::PointCloud2Iterator<uint8_t> iter_g(*(this->pc2), "g");
    sensor_msgs::PointCloud2Iterator<uint8_t> iter_b(*(this->pc2), "b");
    
    float x[2]={9999.99, 0.0}, y[2]={9999.99, 0.0}, z[2]={9999.99, 0.0}, _x, _y, _z;
    uint8_t r[2]={255, 0}, g[2]={255, 0}, b[2]={255, 0};
    double m=(255-50)/(10.15-1.45); // m=y/x
    double c=50-(m*1.45); // y=mx+c
    for(; iter_x != iter_x.end(); ++iter_x, ++iter_y, ++iter_z, ++iter_r, ++iter_g, ++iter_b) {
      _x = *iter_x;
      _y = *iter_y;
      _z = *iter_z;
      *iter_x = (_x * this->rot->getRow(0).x()) + 
                (_y * this->rot->getRow(0).y()) +
                (_z * this->rot->getRow(0).z());
      *iter_y = (_x * this->rot->getRow(1).x()) + 
                (_y * this->rot->getRow(1).y()) +
                (_z * this->rot->getRow(1).z());
      *iter_z = (_x * this->rot->getRow(2).x()) + 
                (_y * this->rot->getRow(2).y()) +
                (_z * this->rot->getRow(2).z());
      *iter_x += 0.45;
      *iter_z += 1.5;

      *iter_r=(m*(*iter_x))+c;
      *iter_g = 0;
      *iter_b = 0;

      if(*iter_x<x[0])
        x[0]=*iter_x;
      if(*iter_y<y[0])
        y[0]=*iter_y;
      if(*iter_z<z[0])
        z[0]=*iter_z;
      if(*iter_r<r[0])
        r[0]=*iter_r;
      if(*iter_g<g[0])
        g[0]=*iter_g;
      if(*iter_b<b[0])
        b[0]=*iter_b;

      if(*iter_x>x[1])
        x[1]=*iter_x;
      if(*iter_y>y[1])
        y[1]=*iter_y;
      if(*iter_z>z[1])
        z[1]=*iter_z;
      if(*iter_r>r[1])
        r[1]=*iter_r;
      if(*iter_g>g[1])
        g[1]=*iter_g;
      if(*iter_b>b[1])
        b[1]=*iter_b;
    }
    RCLCPP_INFO(this->get_logger(), "%lf, %lf, %lf : %lf, %lf, %lf", x[0], y[0], z[0], x[1], y[1], z[1]);
    RCLCPP_INFO(this->get_logger(), "%d, %d, %d : %d, %d, %d", r[0], g[0], b[0], r[1], g[1], b[1]);
    publisher_->publish(*pc2);
  }
  
  void pc2_to_pc(void) {
    //RCLCPP_INFO(this->get_logger(), "pc2_to_pc : start");
    //RCLCPP_INFO(this->get_logger(), "pc2 frame_id : %s", pc2->header.frame_id.c_str());    
    sensor_msgs::convertPointCloud2ToPointCloud(*pc2, *pc);
    pc->header.frame_id = "world";
    //RCLCPP_INFO(this->get_logger(), "pc frame_id : %s", pc->header.frame_id.c_str());
    double x[2]={9999.99, 0.0}, y[2]={9999.99, 0.0}, z[2]={9999.99, 0.0}, _x, _y, _z, v[2]={9999.99, 0.0};
    double m=(3.0-0.0)/(10.15-1.45); // m=y/x
    double b=0.0-(m*1.45); // y=mx+b
    for(unsigned int i=0; i<pc->points.size(); ++i) {
      _x = pc->points[i].x;
      _y = pc->points[i].y;
      _z = pc->points[i].z;
      pc->points[i].x = (_x * this->rot->getRow(0).x()) + 
                        (_y * this->rot->getRow(0).y()) +
                        (_z * this->rot->getRow(0).z());// + 0.45;
      pc->points[i].y = (_x * this->rot->getRow(1).x()) + 
                        (_y * this->rot->getRow(1).y()) +
                        (_z * this->rot->getRow(1).z());
      pc->points[i].z = (_x * this->rot->getRow(2).x()) + 
                        (_y * this->rot->getRow(2).y()) +
                        (_z * this->rot->getRow(2).z());// + 1.5;
      pc->points[i].x += 0.45;
      pc->points[i].z += 1.5;
      if(pc->points[i].x<x[0])
        x[0]=pc->points[i].x;
      if(pc->points[i].y<y[0])
        y[0]=pc->points[i].y;
      if(pc->points[i].z<z[0])
        z[0]=pc->points[i].z;
      if(pc->points[i].x>x[1])
        x[1]=pc->points[i].x;
      if(pc->points[i].y>y[1])
        y[1]=pc->points[i].y;
      if(pc->points[i].z>z[1])
        z[1]=pc->points[i].z;

      pc->channels[0].values[i]=(m*pc->points[i].x)+b;

      if(pc->channels[0].values[i]<v[0])
        v[0]=pc->channels[0].values[i];
      if(pc->channels[0].values[i]>v[1])
        v[1]=pc->channels[0].values[i];
    }
    RCLCPP_INFO(this->get_logger(), "%lf, %lf, %lf : %lf, %lf, %lf : %d, %d", x[0], y[0], z[0], x[1], y[1], z[1], v[0], v[1]);    
    //RCLCPP_INFO(this->get_logger(), "pc2_to_pc : start");
    //publisher_->publish(*pc);
    //RCLCPP_INFO(this->get_logger(), "pc2_to_pc : finished");
  }

  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscription_;
  rclcpp::TimerBase::SharedPtr timer_;

  sensor_msgs::msg::PointCloud2 *pc2;
  sensor_msgs::msg::PointCloud *pc;
  tf2::Quaternion *qBase;
  tf2::Matrix3x3 *rot;
  bool b_run;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<LaneDetection>());
  rclcpp::shutdown();
  return 0;
}
