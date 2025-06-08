document.addEventListener("DOMContentLoaded", function () {
  // 获取所有导航按钮
  const navButtons = document.querySelectorAll(".nav-btn");
  // 获取所有内容区域
  const contentSections = document.querySelectorAll(".content");

  // 为每个按钮添加点击事件
  navButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // 移除所有按钮的active类
      navButtons.forEach((btn) => btn.classList.remove("active"));

      // 为当前点击的按钮添加active类
      this.classList.add("active");

      // 获取要显示的内容区域ID
      const targetId = this.getAttribute("data-target");

      // 隐藏所有内容区域
      contentSections.forEach((section) => {
        section.classList.remove("active");
      });

      // 显示目标内容区域
      const targetContent = document.getElementById(`${targetId}-content`);
      targetContent.classList.add("active");

      // 切换tab时重新渲染图表
      if (targetId === "sports" && typeof window.chart2 !== "undefined") {
        setTimeout(() => {
          // 双重确保容器高度
          const chartContainer = document.getElementById("chart2");
          if (chartContainer.clientHeight === 0) {
            chartContainer.style.height = "600px";
          }

          // 调整图表尺寸
          window.chart2.resize();
        }, 100);
      }
    });
  });

  // 初始加载时检查体育tab
  const activeTab = document.querySelector(".nav-btn.active");
  if (activeTab && activeTab.dataset.target === "sports") {
    setTimeout(() => {
      if (typeof window.chart2 !== "undefined") window.chart2.resize();
    }, 500);
  }
});
