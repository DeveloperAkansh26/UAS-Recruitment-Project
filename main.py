import cv2
import numpy as np


b_lower = np.array([0, 0, 35])
r_lower = np.array([110, 65, 120])


def main():
    n_house_list = []
    priority_list = []
    priority_ratio_dict = {}
    output_img_final = np.array([])

    for i in range(1, 11):
        img = cv2.imread(f"resources/{i}.png")
        n_house, priority, priority_ratio, output_img = result(img)
        output_img = cv2.resize(output_img, (150, 200))

        if i == 1:
            output_img_final = output_img
        else:
            output_img_final = np.hstack((output_img_final, output_img))

        n_house_list.append(n_house)
        priority_list.append(priority)
        priority_ratio_dict[f"image{i}"] = priority_ratio

    print(f"n_houses = {n_house_list}",
          f"priority_houses = {priority_list}",
          f"image_by_rescue_ratio = {sorted(priority_ratio_dict, key=lambda x: priority_ratio_dict[x], reverse=True)}", sep="\n")

    cv2.imshow("Final Output Image", output_img_final)
    cv2.waitKey(0)

    # Individual Image Output Analysis

    # img = cv2.imread("resources/1.png")
    # n_house, priority, priority_ratio, output_img = result(img)
    # print(n_house, priority, priority_ratio)
    # cv2.imshow("output", output_img)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)


def result(img):
    img_blur = cv2.medianBlur(img, 15)

    # Burnt-Green Grass Detection
    kernel = np.ones((5, 5), np.uint8)

    mask_burnt = cv2.inRange(img_blur, b_lower, r_lower)
    mask_burnt = cv2.morphologyEx(mask_burnt, cv2.MORPH_OPEN, kernel)
    mask_burnt = cv2.dilate(mask_burnt, kernel, iterations=7)
    mask_burnt = cv2.erode(mask_burnt, kernel, iterations=8)
    mask_green = cv2.bitwise_not(mask_burnt)

    img_burnt = cv2.bitwise_and(img, img, mask=mask_burnt)
    img_green = cv2.bitwise_and(img, img, mask=mask_green)

    # Red and Blue House Counts
    red_h_b = cv2.inRange(img_burnt, np.array([0, 0, 230]), np.array([0, 0, 255]))
    blue_h_b = cv2.inRange(img_burnt, np.array([230, 0, 0]), np.array([255, 0, 0]))

    red_h_g = cv2.inRange(img_green, np.array([0, 0, 230]), np.array([0, 0, 255]))
    blue_h_g = cv2.inRange(img_green, np.array([230, 0, 0]), np.array([255, 0, 0]))

    red_h_b_c, _ = cv2.findContours(red_h_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    blue_h_b_c, _ = cv2.findContours(blue_h_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    red_h_g_c, _ = cv2.findContours(red_h_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    blue_h_g_c, _ = cv2.findContours(blue_h_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    count = {"red_b": 0, "blue_b": 0, "red_g": 0, "blue_g": 0}

    for ctrs, house_type in zip([red_h_b_c, blue_h_b_c, red_h_g_c, blue_h_g_c], ["red_b", "blue_b", "red_g", "blue_g"]):
        for _ in ctrs:
            count[house_type] += 1

    # Final Result Calculations
    H_b = count["red_b"] + count["blue_b"]
    H_g = count["red_g"] + count["blue_g"]

    P_b = (count["red_b"] * 1) + (count["blue_b"] * 2)
    P_g = (count["red_g"] * 1) + (count["blue_g"] * 2)

    P_r = P_b / P_g

    # Output Image Generation
    burnt_without_h = mask_burnt - red_h_b - blue_h_b
    green_without_h = mask_green - red_h_g - blue_h_g

    color_img = np.zeros(img.shape, np.uint8)
    color_img[:] = [102, 255, 255]
    burnt_color = cv2.bitwise_and(color_img, color_img, mask=burnt_without_h)
    color_img[:] = [255, 255, 102]
    green_color = cv2.bitwise_and(color_img, color_img, mask=green_without_h)

    house_mask = cv2.bitwise_not(burnt_without_h + green_without_h)

    img_bg = burnt_color + green_color
    img_fg = cv2.bitwise_and(img, img, mask=house_mask)

    output_img = img_fg + img_bg

    return [H_b, H_g], [P_b, P_g], P_r, output_img


if __name__ == "__main__":
    main()
