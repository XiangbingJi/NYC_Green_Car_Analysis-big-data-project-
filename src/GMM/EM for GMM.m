clear;
close all

load out.mat
X = traning(:,1:3)';
[d, N] = size(X);
T = 10;
K = 4;
fi_mul_x = zeros(d, 1);
%sigma = [0.9, 0.4;0.4, 0.3];
fi = zeros(N, K);
nn = zeros(K, 1);
sumfi = zeros(K, 1);
pi_m = zeros(K, 1);
%mu_m = zeros(d, K);
sigma_m = ones(d, d, K);
ft = zeros(T, 1);

[labels, mu] = kmeans(X', K);% mu:K*d
mu_m = mu';
Y = X';

for j = 1:K
    sigma_m(:,:,j) = cov(Y(labels == j,:));
    pi_m(j) = sum(labels == j)/N;
end

for t = 1:T
    for j = 1:K
        for i = 1:N
            nor = mvnpdf(X(:,i), mu_m(:,j), sigma_m(:,:,j));
            fi(i,j) = pi_m(j) .* nor;%/sum(pi_m .* nor);%num
        end
    end
    ft(t) = sum(log(sum(fi,2)));
    
    fi = fi./repmat(sum(fi,2),1,K);
    
    for j = 1:K       
        sumfi = sum(fi, 1);
        nn(j) = sumfi(j);
        summ = zeros(d ,1);
        for i = 1:N
            fi_mul_x = fi(i,j).* X(:,i);%d*1
            summ = fi_mul_x + summ;
        end
        mu_m(:,j) = summ./nn(j);%d*1
        
        sumfixx = zeros(d ,d);
        for i = 1:N
            mul = fi(i,j).* ((X(:,i)-mu_m(:,j))*(X(:,i)-mu_m(:,j))');
            sumfixx = sumfixx + mul;
        end
        sigma_m(:,:,j) = sumfixx./nn(j);%d*d
        pi_m(j) = nn(j)/N;
    end    
end

figure;
plot(ft)

fi_t = fi';
[maxnum,I] = max(fi_t);
color = ['r','g','b','c','m','r','g','b','c','m'];
dot = ['.','.','.','.','.','*','*','*','*','*'];

figure;
for i=1:N
    stem3(X(1,i),X(2,i),X(3,i),[color(I(i)) dot(I(i))])
    hold on
end
stem3(mu(:,1),mu(:,2),mu(:,3),['k','x'],'LineWidth',4)


