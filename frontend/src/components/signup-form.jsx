import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { login } from "../services/api";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import Cover from "../assets/welcome-screen.jpg";

export function SignUpForm({ className, ...props }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [serverError, setServerError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: errors[name] }));
    }
  };
  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim())
      newErrors.username = "Введите имя пользователя";
    if (!formData.email.trim()) newErrors.email = "Введите email";
    else if (!/^\S+@\S+\.\S+$/.test(formData.email))
      newErrors.email = "Некорректный email";
    if (!formData.first_name.trim()) newErrors.first_name = "Введите имя";
    if (!formData.last_name.trim()) newErrors.last_name = "Введите фамилию";
    if (!formData.password) newErrors.password = "Введите пароль";
    else if (formData.password.length < 8)
      newErrors.password = "Слишком короткий пароль";
    if (formData.password !== formData.confirmPassword)
      newErrors.confirmPassword = "Пароли не совпадают";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError(null);
    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      const payload = {
        username: formData.username,
        email: formData.email,
        first_name: formData.first_name,
        last_name: formData.last_name,
        password: formData.password,
      };
      const response = await api.post("/users/signup", payload);
      console.log("User created successfully", response.data);
      alert("Поздравляем, вы успешно зарегистрированы!");
      navigate("/login");
    } catch (error) {
      setServerError(
        error.response?.data?.detail ||
          error.response?.data?.message ||
          "Error occurred while creating new user",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={handleSubmit}>
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Регистрация</h1>
                <p className="text-muted-foreground text-balance">
                  Создайте аккаунт "My Whip"
                </p>
              </div>
              <div>
                <div className="flex space-x-4 mb-2">
                  <div className="w-1/2 gap-y-3">
                    <Input
                      name="first_name"
                      placeholder="Имя*"
                      className={errors.first_name ? "border-red-500" : ""}
                      type="text"
                      value={formData.first_name}
                      onChange={handleChange}
                    />
                    <div className="relative">
                      <p
                        className={`absolute text-red-500 text-sm transition-all duration-200 
                            ${errors.first_name ? "opacity-100" : "opacity-0"}`}
                      >
                        {errors.first_name}
                      </p>
                    </div>
                  </div>
                  <div className="w-1/2 gap-y-3">
                    <Input
                      name="last_name"
                      placeholder="Фамилия*"
                      className={errors.last_name ? "border-red-500" : ""}
                      type="text"
                      value={formData.last_name}
                      onChange={handleChange}
                    />
                    <div className="relative">
                      <p
                        className={`absolute text-red-500 text-sm transition-all duration-200 
                            ${errors.last_name ? "opacity-100" : "opacity-0"}`}
                      >
                        {errors.last_name}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="username"></Label>
                  <Input
                    name="username"
                    placeholder="Имя пользователя*"
                    className={errors.username ? "border-red-500" : ""}
                    type="text"
                    value={formData.username}
                    onChange={handleChange}
                  />
                  <div className="relative">
                    <p
                      className={`absolute -top-3 text-red-500 text-sm transition-all duration-200 
                            ${errors.username ? "opacity-100" : "opacity-0"}`}
                    >
                      {errors.username}
                    </p>
                  </div>
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="email" className="font-semibold"></Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="your@mail.com"
                    className={errors.email ? "border-red-500" : ""}
                    value={formData.email}
                    onChange={handleChange}
                  />
                  <div className="relative">
                    <p
                      className={`absolute -top-3 text-red-500 text-sm transition-all duration-200 ${errors.email ? "opacity-100" : "opacity-0"}`}
                    >
                      {errors.email}
                    </p>
                  </div>
                </div>
                <div className="grid gap-3">
                  <div className="flex items-center">
                    <Label htmlFor="password" className="font-semibold"></Label>
                  </div>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Пароль"
                    className={errors.password ? "border-red-500" : ""}
                    value={formData.password}
                    onChange={handleChange}
                  />
                  <div className="relative">
                    <p
                      className={`absolute -top-3 text-red-500 text-sm transition-all duration-200 
                            ${errors.password ? "opacity-100" : "opacity-0"}`}
                    >
                      {errors.password}
                    </p>
                  </div>
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="confirmPassword"></Label>
                  <Input
                    name="confirmPassword"
                    placeholder="Подтвердите пароль*"
                    className={errors.confirmPassword ? "border-red-500" : ""}
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                  />
                  <div className="relative">
                    <p
                      className={`absolute -top-3 text-red-500 text-sm transition-all duration-200 
                            ${errors.confirmPassword ? "opacity-100" : "opacity-0"}`}
                    >
                      {errors.confirmPassword}
                    </p>
                  </div>
                </div>
              </div>

              <Button type="submit" className="w-full" disabled={isSubmitting}>
                {isSubmitting && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                {isSubmitting ? "Регистрация..." : "Зарегистрироваться"}
              </Button>

              <div className="text-center text-sm">
                Уже есть аккаунт?
                <Link to="/login" className="font-bold hover:underline px-1">
                  Войти
                </Link>
              </div>
            </div>
          </form>
          <div className="bg-primary relative hidden md:block">
            <img
              src={Cover}
              alt="Image"
              className="h-full object-cover opacity-50"
            />
          </div>
        </CardContent>
      </Card>
      <div className="text-muted-foreground *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </div>
    </div>
  );
}
